from pydantic import BaseModel


class InterfaceSchema(BaseModel):
    """Basic schema of an interface."""

    id: int
    equipment: int
    date: str
    type: str
    ifIndex: int
    ifName: str
    ifDescr: str
    ifAlias: str
    ifHighSpeed: int
    ifOperStatus: str
    ifAdminStatus: str


class InterfaceChangeSchema(BaseModel):
    """Schema of the interface registered with changes."""

    id: int
    date: str
    ifName: str
    ifDescr: str
    ifAlias: str
    ifHighSpeed: int
    ifOperStatus: str
    ifAdminStatus: str


class RegisterInterfaceBody(BaseModel):
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
