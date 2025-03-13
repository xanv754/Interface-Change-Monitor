from pydantic import BaseModel

class OldInterfaceSchema(BaseModel):
    """Schema of the old interface."""

    id: int
    date: str
    ifName: str
    ifDescr: str
    ifAlias: str
    ifHighSpeed: int
    ifOperStatus: str
    ifAdminStatus: str
                                       

class NewInterfaceSchema(BaseModel):
    """Schema of the new interface."""

    id: int
    date: str
    ifName: str
    ifDescr: str
    ifAlias: str
    ifHighSpeed: int
    ifOperStatus: str
    ifAdminStatus: str

class ChangesResponse(BaseModel):
    """Schema of the changes."""
    id: int
    ip: str
    community: str
    sysname: str
    ifIndex: int
    oldInterface: OldInterfaceSchema
    newInterface: NewInterfaceSchema
    assigned: bool
