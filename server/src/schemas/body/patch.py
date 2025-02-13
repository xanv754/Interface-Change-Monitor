from pydantic import BaseModel


class OperatorUpdateBody(BaseModel):
    username: str
    name: str
    lastname: str
    password: str
    profile: str
    account: str