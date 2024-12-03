from enum import Enum
from pydantic import BaseModel
from database.constants.types.operator import Profile, StatusAccount

class OperatorField(Enum):
    username = "username"
    name = "name"
    lastname = "lastname"
    password = "password"
    profile = "profile"
    statusAccount = "statusAccount"
    deleteOperator = "deleteOperator"

class OperatorEntity(BaseModel):
    username: str
    name: str
    lastname: str
    password: str
    profile: Profile
    statusAccount: StatusAccount
    deleteOperator: bool
