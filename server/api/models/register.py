from pydantic import BaseModel

class RegisterModel(BaseModel):
    name: str
    lastname: str
    username: str
    password: str
    type: str