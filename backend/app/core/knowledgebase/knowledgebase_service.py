from app.core.database.models import KnowledgeBase
from app.core.database.mysql_client import MysqlClient
from fastapi import HTTPException
from app.models.general_models import GenericResponse
from app.core.rag.database.milvus.milvus_client import MilvusCollectionManager
from app.core.rag.database.elasticsearch.elastic_client import ElasticClient
from app.core.rag.rag_pipeline import RAG_Pipeline
from .knowledgebase_type import CreateBaseRequest

from typing import List

class KBase(MysqlClient):
    def __init__(self):
        super().__init__()
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
    
    # 更新知识库
    