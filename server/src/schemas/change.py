from pydantic import BaseModel
from schemas.interface import InterfaceSchema

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


class ChangeSchema(BaseModel):
    """Basic schema of the an change."""

    id: int
    newInterface: int
    oldInterface: int
    operator: str | None


class ChangeInterfaceSchema(BaseModel):
    """Schema of the an change with all information of the interface."""

    id: int
    ip: str
    community: str
    sysname: str
    ifIndex: int
    oldInterface: InterfaceSchema
    newInterface: InterfaceSchema
    operator: str | None


class RegisterChangeBody(BaseModel):
    """Attributes necessary to register an change."""

    newInterface: int
    oldInterface: int