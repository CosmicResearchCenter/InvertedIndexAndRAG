"""
知识库管理部分的路由
"""

from fastapi import APIRouter,File, UploadFile,Form,BackgroundTasks
from app.core.knowledgebase.knowledgebase_service import KBase
from app.core.knowledgebase.knowledgebase_type import CreateBaseRequest,IndexStatusRequest,DocumentSplitArgs
from app.models.general_models import GenericResponse
from typing import List

from concurrent.futures import ThreadPoolExecutor


router = APIRouter()
executor = ThreadPoolExecutor(max_workers=5)

@router.post("/",tags=["创建知识库"],response_model=GenericResponse)
async def create(createBaseRequest:CreateBaseRequest):
    kb = KBase()
    knowledgeBase_id = kb.create_kb(createBaseRequest.base_name)
    return GenericResponse(message="获取成功",code=200,data=[{'knowledgeBase_id':knowledgeBase_id}])

@router.get("/",tags=["获取知识库列表"],response_model=GenericResponse)
async def get_base_list():
    kb_manager = KBase()
    knowledgeBase = kb_manager.get_all_kbs()

    data = []
    for kb in knowledgeBase:
        data.append(kb.to_dict())

    return GenericResponse(message="获取成功",code=200,data=data)


@router.get("/{base_id}",tags=["获取知识库详情"],response_model=GenericResponse)
async def get_base_detail(base_id:str):
    kb_manager = KBase()
    infos = kb_manager.get_kbinfo_by_id(base_id)
    infos_prased = []
    for index_info in infos:
        info = {
            'create_time':index_info.create_time,
            'doc_name':index_info.doc_name,
            'doc_id':index_info.save_id,
            'doc_size':index_info.doc_size,
        }
        infos_prased.append(info)
    return GenericResponse(message="获取成功",code=200,data=infos_prased)

@router.put("/{base_id}",tags=["更新知识库"],response_model=GenericResponse)
async def upload(
    base_id:str,
    background_tasks: BackgroundTasks,
    file:UploadFile = File(...),
    ):
    print("uploading file")
    if file == None:
        return GenericResponse(message="文件不能为空",code=400,data=[])
    
    base_id = base_id
 
    if base_id == "":
        return GenericResponse(message="知识库ID不能为空",code=400,data=[])
    
    kb_manager = KBase()

    # index_infos = await  kb_manager.upload_files(base_id,file,threadPool)
    index_infos =   kb_manager.upload_files(base_id,[file],background_tasks,executor)

    index_infos_prase = []
    for index_info in index_infos:
        info = {
            'doc_id':index_info.doc_id,
            'index_status':index_info.index_status,
            'knowledgeBaseId':index_info.knowledgeBaseId
        }
        index_infos_prase.append(info)


    return GenericResponse(message="上传成功",code=200,data=index_infos_prase)

@router.post("/{base_id}/doc/{doc_id}/index",tags=["插入文档到知识库"],response_model=GenericResponse)
def insert_doc(base_id:str,doc_id:str,documentSplitArgs:DocumentSplitArgs,background_tasks: BackgroundTasks):
    kb_manager = KBase()
    index_status = kb_manager.insert_knowledgebase(documentSplitArgs,base_id,doc_id,background_tasks,executor)
    return GenericResponse(message="正在建立索引",code=200,data=[index_status.to_dict()])


@router.get("/{base_id}/doc/{doc_id}/index_status", tags=["获取文档索引状态"],response_model=GenericResponse)
async def get_doc_index_status(base_id:str, doc_id:str):
    kb_manager = KBase()
    index_status = kb_manager.get_index_status(base_id,doc_id)

    return GenericResponse(message="获取成功",code=200,data=[index_status.to_dict()])


@router.delete("/{base_id}",tags=["删除知识库"],response_model=GenericResponse)
async def delete(base_id:str):
    kb_manager = KBase()
    return kb_manager.delete_kb(base_id)


@router.delete("/{base_id}/doc/{doc_id}",tags=["删除文档"],response_model=GenericResponse)
async def delete_doc():
    pass