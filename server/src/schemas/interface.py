from pydantic import BaseModel


class InterfaceSchema(BaseModel):
    """Schema of an interface in the database."""

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
