from pydantic import BaseModel

class AccessModel(BaseModel):
    access_token: str
    token_type: str