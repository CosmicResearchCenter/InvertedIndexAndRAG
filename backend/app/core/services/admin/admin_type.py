from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime
class SystemInfo(BaseModel):
    knowledge_base_count: int
    user_count: int
    conversation_count: int
    
    
class User(BaseModel):
    username:str
    admin_sign: bool

    
class Message(BaseModel):
    assistant: str
    message_time: Optional[str] = None
    user: str 
    
class Conversation_Collection(BaseModel):
    conversation_title: Optional[str] = None
    conversation_time: str
    conversation_id: int
    delete_sign: bool
    



class KnowledgeBaseInfo(BaseModel):
    knowledge_base_id: str
    knowledge_base_name: str
    docs_num: int
    words_num: int
    related_conversations: int
    delete_sign: bool
    # create_time: str
    # update_time: str
    created_by: str
    
    create_time: datetime  # 直接使用 datetime 类型
    update_time: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()  # JSON序列化时自动转换为ISO格式
        }
    
class KnowledgeBaseItem(BaseModel):
    knowledge_base_id: str
    knowledge_base_name: str
    knowledge_base_info : KnowledgeBaseInfo
    
class DocInfo_Re(BaseModel):
    doc_id: str
    doc_name: str
    doc_type: str
    doc_size: int
    delete_sign: bool
    retriever_num: int