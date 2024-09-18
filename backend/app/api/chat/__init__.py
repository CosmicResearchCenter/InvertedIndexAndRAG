"""
对话部分的路由
"""

from fastapi import APIRouter
from starlette.responses import StreamingResponse
from app.models.chat_models import Query,ResultByKnowledgeBase,Answer
from app.core.rag.rag_pipeline import RAG_Pipeline

router = APIRouter()

@router.post("/chat")
async def chat(query: Query):
    # 获取知识库id
    knowledge_base_id = query.knowledge_base_id
    # 获取对话id，如果为空则生成对话id，否则使用已有的对话id加载聊天记录
    conversation_id = query.conversation_id
    if not conversation_id:
        conversation_id = ""
    
    # 进行指代替换


    # 调用RAG_Pipeline生成答案


    pass

