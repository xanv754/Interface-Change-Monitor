from pydantic import BaseModel

class Interface(BaseModel):
    ip: str
    community: str
    ifIndex: str
    ifName: str
    ifDescr: str
    ifAlias: str
    ifHighSpeed: str
    ifOperStatus: str
    ifAdminStatus: str