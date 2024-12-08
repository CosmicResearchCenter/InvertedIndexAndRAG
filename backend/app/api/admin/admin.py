from pydantic import BaseModel
from typing import List,Any

class ResponseGenral(BaseModel):
    code: int
    message: str
    data: List[Any]