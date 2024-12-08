from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime
class SystemInfo(BaseModel):
    knowledge_base_count: int
    user_count: int
    conversation_count: int
    
    


    
class Message(BaseModel):
    assistant: str
    message_time: Optional[str] = None
    user: str 
    
class ConversationSession(BaseModel):
    message_count: int
    content: List[Message]
    

class Conversation_Collection(BaseModel):
    conversation_title: str
    conversation_content: ConversationSession
    conversation_time: str
    conversation_id: str
    
class UserConversation(BaseModel):
    username: str
    conversation_collection: List[Conversation_Collection] 


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
    
class User_KnowledgeBase(BaseModel):
    knowledge_base_list: List[KnowledgeBaseItem]
    username: str