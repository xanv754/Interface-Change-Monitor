from pydantic import BaseModel


class InterfaceField:
    ID = "id"
    IP = "ip"
    COMMUNITY = "community"
    SYSNAME = "sysname"
    IFINDEX = "ifIndex"
    IFNAME = "ifName"
    IFDESCR = "ifDescr"
    IFALIAS = "ifAlias"
    IFHIGHSPEED = "ifHighSpeed"
    IFOPERSTATUS = "ifOperStatus"
    IFADMINSTATUS = "ifAdminStatus"
    CONSULTED_AT = "consulted_at"


class InterfaceModel(BaseModel):
    id: int | None
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
    consulted_at: str