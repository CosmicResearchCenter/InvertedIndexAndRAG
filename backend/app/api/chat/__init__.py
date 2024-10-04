"""
对话部分的路由
"""

from fastapi import APIRouter
from starlette.responses import StreamingResponse
from app.models.chat_models import ChatMessageRequest,ChatClearResponse,ChatMessageResponse,ChatMessageHistoryResponse,ConversationCreateRequest,ConversationCreateResponse,ChatConversationResponse
from app.core.rag.rag_pipeline import RAG_Pipeline
from app.core.chat.chat import Chat
from app.core.database.models import Chat_Messages
from typing import List
router = APIRouter()

@router.get("/chat-history/{conversation_id}",response_model=ChatMessageHistoryResponse)
def chat_history(conversation_id: str):
    chat:Chat = Chat(conversation_id,"")
    chat_history = chat.load_conversation(conversation_id)

    return ChatMessageHistoryResponse(data=chat_history,code = 200,message="Get chat history successfully!")

@router.post("/chat-message", response_model=ChatMessageResponse)
def chat(query: ChatMessageRequest):
    # 获取对话id，如果为空则生成对话id，否则使用已有的对话id加载聊天记录
    conversation_id = query.conversation_id
    if not conversation_id:
        return ChatMessageResponse(code=400,message="Conversation id is required")
    
    chat:Chat = Chat(conversation_id,query.user_id)

    try:
        result = chat.run(query)
        if result == None:
            raise Exception("No results found.")
        del chat
        return ChatMessageResponse(data=result,code = 200,message="Get chat message successfully!")
    except Exception as e:
        print(e)
        return ChatMessageResponse(code=400,message="No results found.")
@router.post("/create-conversation",response_model=ConversationCreateResponse)
def create_conversation(conversationCreateRequest: ConversationCreateRequest):
    chat:Chat = Chat(conversation_id="",user_id=conversationCreateRequest.user_id)

    try:
        print(conversationCreateRequest.knowledge_base_id)
        conversation = chat.create_conversation(
            knowledgeBaseId=conversationCreateRequest.knowledge_base_id,
            user_id=conversationCreateRequest.user_id
            )
        del chat
        return ConversationCreateResponse(data=conversation.to_dict(),code = 200,message="Create conversation successfully!" )
    except Exception as e:
        # print(e)
        return ConversationCreateResponse(code=400,message="Failed to create conversation")
# 获取对话列表
@router.get("/chat-message/{user_id}",response_model=ChatConversationResponse)
def chat_message(user_id: str):
    chat:Chat = Chat(conversation_id="",user_id=user_id)
    conversations = chat.get_conversation_list(user_id)
    conversations_prased = [conversation.to_dict() for conversation in conversations]

    return ChatConversationResponse(data=conversations_prased,code = 200,message="Get chat message successfully!" )


@router.post("/knowledge_base", response_model=ChatMessageResponse)
def knowledge_base(query: ChatMessageRequest):
    return {"code": 200}


@router.post("/chat-clear", response_model=ChatClearResponse)
def clear():
    return {"code": 200}



