from app.core.rag.database.mysql.model import KnowledgeBase
from app.core.database.models import DocInfo,DocIndexStatus
from app.core.database.mysql_client import MysqlClient
from fastapi import HTTPException
from app.models.general_models import GenericResponse
from app.core.rag.database.milvus.milvus_client import MilvusCollectionManager
from app.core.rag.database.elasticsearch.elastic_client import ElasticClient
from app.core.rag.rag_pipeline import RAG_Pipeline
from .knowledgebase_type import CreateBaseRequest,IndexStatusRequest
from fastapi import UploadFile,BackgroundTasks
from typing import List
import os
import shutil
import time
from pathlib import Path
import uuid
import asyncio
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'docx','doc','ppt','pptx','excel'}

class KBase(MysqlClient):
    def __init__(self):
        super().__init__()
        self.index_status = False
    def __del__(self):
        super().__del__()
    # 创建知识库
    def create_kb(self, kb_name:str)->KnowledgeBase:
        rAG_Pipeline:RAG_Pipeline = RAG_Pipeline()
        return rAG_Pipeline.create_knowledgebase(kb_name)
    # 获取所有知识库
    def get_all_kbs(self)->List[KnowledgeBase]:
        # all_kbs = self.db.query(KnowledgeBase).all()
        rAG_Pipeline:RAG_Pipeline = RAG_Pipeline()
        try:
            all_kbs = rAG_Pipeline.show_knowledgebase_list()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        return all_kbs
    
    # 根据id获取知识库
    def get_kb_by_id(self, kb_id:int)->KnowledgeBase:
        kb = self.db.query(KnowledgeBase).filter(KnowledgeBase.id == kb_id).first()
        return kb
    # 删除知识库
    def delete_kb(self, kb_id:int)->GenericResponse:
        # 删除表
        kb = self.get_kb_by_id(kb_id)
        if not kb:
            return GenericResponse(message="KnowledgeBase not found", code=404)
        self.db.delete(kb)
        
        # 删除ElasticSearch数据
        try:
            elastic_client = ElasticClient()
            elastic_client.delete_index(kb_id)
        except Exception as e:
            print("Error deleting index from ElasticSearch: ", e)
            return GenericResponse(message="KnowledgeBase not found", code=404)
        # 删除Milvus数据
        try:
            milvus_manager = MilvusCollectionManager()
            milvus_manager.drop_collection(f'{kb_id}')
        except Exception as e:
            print("Error dropping collection from Milvus: ", e)
            return GenericResponse(message="KnowledgeBase not found", code=404)
        
        return GenericResponse(message="KnowledgeBase deleted successfully", code=200)
    def _get_docs_save_path(self, base_id:int)->Path:
        from config.config import DOCS_PATH
        save_path_p = Path(DOCS_PATH)/ base_id
        if not os.path.exists(save_path_p):
            os.makedirs(save_path_p)
        return save_path_p
    # 更新知识库
    # 为每个文档生成一个信息字典，包括文档id、文档名称、文档类型等信息，保存到数据库中
    async def upload_files(self, base_id:int, files:List[UploadFile],backgroundTasks:BackgroundTasks)->List[DocIndexStatus]:
        from config.config import DOCS_PATH
        save_path_p = self._get_docs_save_path(base_id)
        docs:List[DocInfo] = []
        docs_status:List[DocIndexStatus] = []
        for file in files:
            doc_name = file.filename
            extension = file.filename.split('.')[-1]
            if extension not in ALLOWED_EXTENSIONS:
                raise HTTPException(status_code=400, detail=f"Invalid file extension: {extension}")

            create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            doc_size = file.size
            
            save_id = str(uuid.uuid4())
       
            doc_newname = f'{save_id}.{extension}'

            save_path = Path(save_path_p)/ doc_newname

            # 保存文件到本地
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            doc = DocInfo(doc_name=doc_name, doc_type=extension, doc_size=doc_size, create_time=create_time, knowledgeBaseId=base_id,save_id=save_id)
            
            self.db.add(doc)
            self.db.commit()
            docs.append(doc)

            index_status = DocIndexStatus(index_status=0,knowledgeBaseId=base_id,doc_id=save_id)
            self.db.add(index_status)
            self.db.commit()

            docs_status.append(index_status)

            backgroundTasks.add_task(self.insert_knowledgebase,base_id,doc)
            # asyncio.create_task( self.insert_knowledgebase(base_id,doc))
            print(f'{len(files)} files saved successfully')
        return docs_status
    
    # 解析文档
    async def insert_knowledgebase(self, base_id:int,doc:DocInfo):
        print(f'insert_knowledgebase document {doc.doc_name}')
        rAG_Pipeline:RAG_Pipeline = RAG_Pipeline()

        save_path_p = self._get_docs_save_path(base_id)

        doc_newname = f'{doc.save_id}.{doc.doc_type}'
        doc_path = Path(save_path_p)/ doc_newname
        try:
            rAG_Pipeline.insert_knowledgebase(str(doc_path),base_id)
        except Exception as e:
            print(f"Error parsing document {doc.doc_name}: {e}")

        index_status = self.db.query(DocIndexStatus).filter(DocIndexStatus.knowledgeBaseId == base_id,DocIndexStatus.doc_id==doc.save_id).first()
        if index_status:
            index_status.index_status = 1
            self.db.commit()
            self.db.refresh(index_status)
            

    def get_index_status(self, base_id:str,doc_id:str)->DocIndexStatus:
        index_status = self.db.query(DocIndexStatus).filter(DocIndexStatus.knowledgeBaseId == base_id,DocIndexStatus.doc_id==doc_id).first()
        if not index_status:
            raise HTTPException(status_code=404, detail="Index status not found")
        return index_status