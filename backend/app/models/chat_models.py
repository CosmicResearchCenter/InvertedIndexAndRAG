from pydantic import BaseModel
from typing import List, Optional,Dict
from app.core.rag.models.knolwedge_base import ResultByDoc
from app.core.chat.chat_type import ChatMessageHistory
# Chat message request
class ChatMessageRequest(BaseModel):
    conversation_id: str
    message: str
    user_id: str

# Chat message history response
class ChatMessageHistoryResponse(BaseModel):
    code: int
    data: List[ChatMessageHistory]
    message: str

class ChatMessageResponse(BaseModel):
    code: int
    data: ResultByDoc
    message: str

class ConversationCreateRequest(BaseModel):
    user_id: str
    knowledge_base_id: str

class ConversationCreateResponse(BaseModel):
    code: int
    data: Optional[dict]
    message: str

# Knowledge base selection request
class KnowledgeBaseSelectRequest(BaseModel):
    conversation_id: str
    knowledge_base_id: str

# Knowledge base selection response
class KnowledgeBaseSelectResponse(BaseModel):
    code: int
    data: List[Optional[dict]]
    message: str

# Clear chat request
class ChatClearRequest(BaseModel):
    conversation_id: str

# Clear chat response
class ChatClearResponse(BaseModel):
    code: int
    data: List[Optional[dict]]
    message: str

# Create knowledge base request
class CreateKnowledgeBaseRequest(BaseModel):
    name: str

# Create knowledge base response
class CreateKnowledgeBaseResponse(BaseModel):
    code: int
    data: List[Optional[dict]]
    message: str

# Knowledge base list response
class KnowledgeBaseListResponse(BaseModel):
    code: int
    data: List[Optional[dict]]
    message: str

# Knowledge base details response
class KnowledgeBaseDetailResponse(BaseModel):
    code: int
    data: List[Optional[dict]]
    message: str

# Upload file request
class UploadFileRequest(BaseModel):
    file: str

# Upload file response
class UploadFileResponse(BaseModel):
    code: int
    data: List[Optional[dict]]
    message: str

# File index status response
class FileIndexStatusResponse(BaseModel):
    code: int
    data: List[Optional[dict]]
    message: str
