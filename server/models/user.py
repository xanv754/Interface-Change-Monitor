from pydantic import BaseModel


class UserField:
    USERNAME = "username"
    PASSWORD = "password"
    NAME = "name"
    LASTNAME = "lastname"
    STATUS = "status"
    ROLE = "role"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class UserModel(BaseModel):
    username: str
    password: str
    name: str
    lastname: str
    status: str
    role: str
    created_at: str | None
    updated_at: str | None