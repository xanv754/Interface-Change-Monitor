from pydantic import BaseModel


class EquipmentRegisterBody(BaseModel):
    """Attributes necessary to register an equipment."""

    ip: str
    community: str
    sysname: str | None = None


class AssignmentRegisterBody(BaseModel):
    """Attributes necessary to register an assignment."""

    newInterface: int
    oldInterface: int
    operator: str
    assignedBy: str


class OperatorRegisterBody(BaseModel):
    """Attributes necessary to register an operator."""

    username: str
    name: str
    lastname: str
    password: str
    profile: str


class InterfaceRegisterBody(BaseModel):
    """Attributes necessary to register an interface."""

    dateConsult: str
    interfaceType: str
    ip: str
    community: str
    sysname: str
    ifIndex: int
    ifName: str
    ifDescr: str
    ifAlias: str
    ifHighSpeed: int
    ifOperStatus: str
    ifAdminStatus: str
