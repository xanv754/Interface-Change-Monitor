from pydantic import BaseModel


class OperatorSchema(BaseModel):
    username: str
    name: str
    lastname: str
    password: str
    profile: str
    account: str
    created_at: str