from pydantic import BaseModel
from typing import List
from .source_document import SourceDocument

class ResultByDoc(BaseModel):
    source:List[SourceDocument]
    answer:str
