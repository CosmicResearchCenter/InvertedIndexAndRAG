from pydantic import BaseModel
from typing import Any,List, Optional,Dict

class Query(BaseModel):
    query: str = None,
    knowledge_base_id: str = None
    user_id: str = None
    conversation_id: str = None
class Answer(BaseModel):
    answer: str = None
    conversation_id: str = None
    def to_dict(self):
        return {
            "answer": self.answer,
            "conversation_id": self.conversation_id
        }
class ResultByKnowledgeBase(BaseModel):
    code:str
    data:List[Dict]
    message:str
