from  pydantic import BaseModel
class SourceDocument:
    content: str
    knowledge_doc_name: str
    
    def __init__(self, content:str, knowledge_doc_name: str):
        self.content = content
        self.knowledge_doc_name = knowledge_doc_name