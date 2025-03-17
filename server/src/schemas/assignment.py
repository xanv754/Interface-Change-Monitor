from typing import List
from pydantic import BaseModel


class AssignmentSchema(BaseModel):
    """Basic schema of the assignment."""

    id: int
    newInterface: int
    oldInterface: int
    operator: str
    date: str
    status: str
    assignedBy: str
    updatedAt: str | None


class AssignmentInterfaceSchema(BaseModel):
    """Schema of the assignment with all the information of the interface."""
    idAssignment: int
    dateAssignment: str
    statusAssignment: str
    assignedBy: str
    updateAt: str | None
    oldIfName: str
    oldIfDescr: str
    oldIfAlias: str
    oldIfHighSpeed: int
    oldIfOperStatus: str
    oldIfAdminStatus: str
    newIfName: str
    newIfDescr: str
    newIfAlias: str
    newIfHighSpeed: int
    newIfOperStatus: str
    newIfAdminStatus: str
    ip: str
    community: str
    sysname: str
    ifIndex: int


class AssignmentInterfaceAssignedSchema(BaseModel):
    """Schema of the assignment with all the information of the interface and the operator assigned."""
    idAssignment: int
    dateAssignment: str
    statusAssignment: str
    assignedBy: str
    updateAt: str | None
    oldIfName: str
    oldIfDescr: str
    oldIfAlias: str
    oldIfHighSpeed: int
    oldIfOperStatus: str
    oldIfAdminStatus: str
    newIfName: str
    newIfDescr: str
    newIfAlias: str
    newIfHighSpeed: int
    newIfOperStatus: str
    newIfAdminStatus: str
    ip: str
    community: str
    sysname: str
    ifIndex: int
    username: str | None
    name: str | None
    lastname: str | None


class AssignmentStatisticsSchema(BaseModel):
    """Schema of the statistics of the assignments."""

    username: str
    name: str
    lastname: str
    totalPending: int
    totalRevised: int


class UpdateStatusAssignmentBody(BaseModel):
    """Attributes necessary to update the status of an assignment."""

    idAssignment: int
    newStatus: str


class ReassignBody(BaseModel):
    """Attributes necessary to reassign an assignment."""
    
    idAssignment: int
    newOperator: str
    assignedBy: str


class RegisterAssignmentBody(BaseModel):
    """Attributes necessary to register an assignment."""

    idChange: int
    newInterface: int
    oldInterface: int
    operator: str
    assignedBy: str

class RegisterAutoAssignment(BaseModel):
    """Attributes necessary to register automatically assignments."""

    users: List[str]
    assignedBy: str