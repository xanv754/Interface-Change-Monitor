from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    password: str
    name: str
    lastname: str
    status: str
    role: str
    created_at: str | None
    updated_at: str | None