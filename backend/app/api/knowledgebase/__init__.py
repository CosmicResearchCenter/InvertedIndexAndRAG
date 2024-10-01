"""
知识库管理部分的路由
"""

from fastapi import APIRouter
from app.core.knowledgebase.knowledgebase_service import KBase
from app.core.knowledgebase.knowledgebase_type import CreateBaseRequest
from app.models.general_models import GenericResponse
router = APIRouter()

@router.post("/",tags=["创建知识库"],response_model=GenericResponse)
def create(createBaseRequest:CreateBaseRequest):
    kb = KBase()
    knowledgeBase_id = kb.create_kb(createBaseRequest.base_name)
    GenericResponse(message="获取成功",code=200,data={'knowledgeBase_id':knowledgeBase_id})
@router.get("/",tags=["获取知识库列表"],response_model=GenericResponse)
def get_base_list():
    kb_manager = KBase()
    knowledgeBase = kb_manager.get_all_kbs()

    data = []
    for kb in knowledgeBase:
        data.append(kb.to_dict())

    return GenericResponse(message="获取成功",code=200,data=data)
@router.get("/{base_id}",tags=["获取知识库详情"],response_model=GenericResponse)
def get_base_detail():
    pass
@router.put("/{base_id}",tags=["更新知识库"],response_model=GenericResponse)
def update():
    pass

@router.get("/{base_id}/doc/{doc_id}/index_status", tags=["获取文档索引状态"],response_model=GenericResponse)
def get_doc_index_status():
    pass

@router.delete("/{base_id}",tags=["删除知识库"],response_model=GenericResponse)
def delete():
    pass

@router.delete("/{base_id}/doc/{doc_id}",tags=["删除文档"],response_model=GenericResponse)
def delete_doc():
    pass