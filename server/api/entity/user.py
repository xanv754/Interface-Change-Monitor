from models.interface import InterfaceModel
from constants.userStatus import userstatus
from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: (str | None) = None
    username: str
    password: str
    lastPassword: (str | None) = None
    name: str
    lastname: str
    type: str
    assigned: List[InterfaceModel] = []
    status: str = userstatus.pending
