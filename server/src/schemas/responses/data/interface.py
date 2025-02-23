from pydantic import BaseModel


class InterfaceResponseSchema(BaseModel):
    """Schema of the interface."""

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
