from pydantic import BaseModel

class SNMPModel(BaseModel):
    date: str
    ip: str
    community: str
    sysname: str
    ifIndex: str
    ifName: str
    ifAlias: str
    ifDescr: str
    ifSpeed: str
    ifHighSpeed: str
    ifPhysAddress: str
    ifType: str
    ifOperStatus: str
    ifAdminStatus: str
    ifLastChange: str
    ifPromiscuousMode: str
    ifConnectorPresent: str
