from pydantic import BaseModel


class OperatorUpdatePassword(BaseModel):
    password: str


class OperatorUpdateProfile(BaseModel):
    username: str
    profile: str


class OperatorUpdateAccount(BaseModel):
    username: str
    account: str

class AssignmentUpdateStatus(BaseModel):
    id: int
    new_status: str


class AssignmentReassignBody(BaseModel):
    id_assignment: int
    new_operator: str
    assigned_by: str