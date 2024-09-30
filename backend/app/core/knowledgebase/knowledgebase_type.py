from pydantic import BaseModel

class CreateBaseRequest(BaseModel):
    base_name: str