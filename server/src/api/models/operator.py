from pydantic import BaseModel

class OperatorBodyModel(BaseModel):
    username: str
    name: str
    lastname: str
    password: str
    profile: str