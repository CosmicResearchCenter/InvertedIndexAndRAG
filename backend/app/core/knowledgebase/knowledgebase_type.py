from pydantic import BaseModel

class CreateBaseRequest(BaseModel):
    base_name: str

class UploadFileRequest(BaseModel):
    base_id: int
    
class IndexStatusRequest(BaseModel):
    base_id: str