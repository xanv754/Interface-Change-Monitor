from pydantic import BaseModel


class EquipmentRegisterRequest(BaseModel):
    ip: str
    community: str
    sysname: str


class AssignmentRegisterRequest(BaseModel):
    change_interface: int
    old_interface: int
    operator: str
    assigned_by: str


class OperatorRegisterBody(BaseModel):
    username: str
    name: str
    lastname: str
    password: str
    profile: str