from pydantic import BaseModel


class ChangeField:
    CURRENT_INTERFACE_ID = "current_interface_id"
    OLD_INTERFACE_ID = "old_interface_id"
    ASSIGNED = "assigned"


class ChangeCompleteField:
    ID_OLD = "id_old"
    IP_OLD = "ip_old"
    COMMUNITY_OLD = "community_old"
    SYSNAME_OLD = "sysname_old"
    IFINDEX_OLD = "ifIndex_old"
    IFNAME_OLD = "ifName_old"
    IFDESCR_OLD = "ifDescr_old"
    IFALIAS_OLD = "ifAlias_old"
    IFHIGHSPEED_OLD = "ifHighSpeed_old"
    IFOPERSTATUS_OLD = "ifOperStatus_old"
    IFADMINSTATUS_OLD = "ifAdminStatus_old"
    ID_NEW = "id_new"
    IP_NEW = "ip_new"
    COMMUNITY_NEW = "community_new"
    SYSNAME_NEW = "sysname_new"
    IFINDEX_NEW = "ifIndex_new"
    IFNAME_NEW = "ifName_new"
    IFDESCR_NEW = "ifDescr_new"
    IFALIAS_NEW = "ifAlias_new"
    IFHIGHSPEED_NEW = "ifHighSpeed_new"
    IFOPERSTATUS_NEW = "ifOperStatus_new"
    IFADMINSTATUS_NEW = "ifAdminStatus_new"
    USERNAME = "username"
    NAME = "name"
    LASTNAME = "lastname"


class ChangeModel(BaseModel):
    current_interface_id: int
    old_interface_id: int
    assigned: str
    

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