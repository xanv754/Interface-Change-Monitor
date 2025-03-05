from pydantic import BaseModel


class AssignmentResponseSchema(BaseModel):
    """Schema of the assignment."""

    id: int
    newInterface: int
    oldInterface: int
    operator: str
    date: str
    status: str
    assignedBy: str
    updatedAt: str | None


class AssignmentInterfaceResponseSchema(BaseModel):
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
