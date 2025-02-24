from pydantic import BaseModel


class OperatorUpdatePassword(BaseModel):
    """Attributes necessary to update the password of an operator."""

    password: str


class OperatorUpdateProfile(BaseModel):
    """Attributes necessary to update the profile of an operator."""

    username: str
    profile: str


class OperatorUpdateAccount(BaseModel):
    """Attributes necessary to update the account of an operator."""

    username: str
    account: str


class AssignmentUpdateStatus(BaseModel):
    """Attributes necessary to update the status of an assignment."""

    idAssignment: int
    newStatus: str


class AssignmentReassignBody(BaseModel):
    """Attributes necessary to reassign an assignment."""

    idAssignment: int
    newOperator: str
    assignedBy: str
