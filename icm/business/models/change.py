from pydantic import BaseModel


class ChangeModel(BaseModel):
    id_old: int
    ip_old: str
    community_old: str
    sysname_old: str
    ifIndex_old: int
    ifName_old: str | None 
    ifDescr_old: str | None
    ifAlias_old: str | None
    ifHighSpeed_old: str | None
    ifOperStatus_old: str | None
    ifAdminStatus_old: str | None
    id_new: int
    ip_new: str
    community_new: str
    sysname_new: str
    ifIndex_new: int
    ifName_new: str | None
    ifDescr_new: str | None
    ifAlias_new: str | None
    ifHighSpeed_new: str | None
    ifOperStatus_new: str | None
    ifAdminStatus_new: str | None
    username: str | None
    name: str | None
    lastname: str | None


class UpdateChangeModel(BaseModel):
    id_old: int
    id_new: int
    username: str