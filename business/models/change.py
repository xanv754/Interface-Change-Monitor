from pydantic import BaseModel


class ChangeModel(BaseModel):
    id_old: int
    ip_old: str
    community_old: str
    sysname_old: str
    ifIndex_old: int
    ifName_old: str
    ifDescr_old: str
    ifAlias_old: str
    ifHighSpeed_old: int
    ifOperStatus_old: str
    ifAdminStatus_old: str
    id_new: int
    ip_new: str
    community_new: str
    sysname_new: str
    ifIndex_new: int
    ifName_new: str
    ifDescr_new: str
    ifAlias_new: str
    ifHighSpeed_new: int
    ifOperStatus_new: str
    ifAdminStatus_new: str
    assigned: str | None
    

class ChangeCompleteModel(BaseModel):
    id_old: int
    ip_old: str
    community_old: str
    sysname_old: str
    ifIndex_old: int
    ifName_old: str
    ifDescr_old: str
    ifAlias_old: str
    ifHighSpeed_old: int
    ifOperStatus_old: str
    ifAdminStatus_old: str
    id_new: int
    ip_new: str
    community_new: str
    sysname_new: str
    ifIndex_new: int
    ifName_new: str
    ifDescr_new: str
    ifAlias_new: str
    ifHighSpeed_new: int
    ifOperStatus_new: str
    ifAdminStatus_new: str
    username: str | None
    name: str | None
    lastname: str | None