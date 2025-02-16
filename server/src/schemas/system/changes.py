from pydantic import BaseModel
from schemas import InterfaceSchema

class OldInterfaceSchema(BaseModel):
    """Schema of the old interface."""

    id: int
    date: str
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


class NewInterfaceSchema(BaseModel):
    """Schema of the new interface."""

    id: int
    date: str
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

class ChangesSchema(BaseModel):
    """Schema of the changes."""

    ip: str
    community: str
    sysname: str
    ifIndex: int
    old_interface: OldInterfaceSchema
    new_interface: NewInterfaceSchema
