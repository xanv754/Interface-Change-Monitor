from pydantic import BaseModel


class OperatorUpdateBody(BaseModel):
    username: str
    name: str
    lastname: str
    profile: str
    account: str


class OperatorUpdateStandardBody(BaseModel):
    name: str
    lastname: str