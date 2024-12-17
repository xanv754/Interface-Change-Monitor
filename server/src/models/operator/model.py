from pydantic import BaseModel

class OperatorModel(BaseModel):
    username: str
    name: str
    lastname: str
    password: str
    profile: str
    statusaccount: str
    createdat: str | None