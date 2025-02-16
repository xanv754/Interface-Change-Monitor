from pydantic import BaseModel


class EquipmentRegisterBody(BaseModel):
    ip: str
    community: str
    sysname: str | None = None


class AssignmentRegisterBody(BaseModel):
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


class InterfaceRegisterBody(BaseModel):
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
    ifLastCheck: str
