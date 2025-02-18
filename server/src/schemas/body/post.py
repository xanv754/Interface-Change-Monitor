from pydantic import BaseModel


class EquipmentRegisterBody(BaseModel):
    """Attributes necessary to register an equipment."""

    ip: str
    community: str
    sysname: str | None = None


class AssignmentRegisterBody(BaseModel):
    """Attributes necessary to register an assignment."""

    change_interface: int
    old_interface: int
    operator: str
    assigned_by: str


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
    ifSpeed: int
    ifHighSpeed: int
    ifPhysAddress: str
    ifType: str
    ifOperStatus: str
    ifAdminStatus: str
    ifPromiscuousMode: bool
    ifConnectorPresent: bool
    ifLastChange: str
