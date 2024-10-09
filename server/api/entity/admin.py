from constants.userStatus import userstatus
from pydantic import BaseModel

class Admin(BaseModel):
    id: (str | None) = None
    username: str
    password: str
    lastPassword: (str | None) = None
    name: str
    lastname: str
    type: str
    status: str = userstatus.pending
