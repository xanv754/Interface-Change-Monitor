from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from libs.types.profile import ProfileType
from libs.types.account import AccountType

class OperatorEntity(BaseModel):
    username: str
    name: str
    lastname: str
    password: str
    profile: ProfileType
    statusaccount: AccountType
    createdat: datetime

class OperatorField(Enum):
    username = 'username'
    name = 'name'
    lastname = 'lastname'
    password = 'password'
    profile = 'profile'
    statusAccount = 'statusaccount'
    createdAt = 'createdat'