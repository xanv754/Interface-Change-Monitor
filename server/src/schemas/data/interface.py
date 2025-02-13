from pydantic import BaseModel


class InterfaceSchema(BaseModel):
    id: int
    equipment: int
    date: str
    type: str
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