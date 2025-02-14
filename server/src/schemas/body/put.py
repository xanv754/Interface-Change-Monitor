from pydantic import BaseModel


class AssignmentUpdateStatus(BaseModel):
    id: int
    new_status: str


class OperatorUpdatePassword(BaseModel):
    password: str