from pydantic import BaseModel
from database.constants.profile import TypeProfile
from database.constants.account import TypeStatusAccount

class OperatorEntity(BaseModel):
    username: str
    name: str
    lastname: str
    password: str
    profile: TypeProfile
    statusAccount: TypeStatusAccount
    deleteOperator: bool
