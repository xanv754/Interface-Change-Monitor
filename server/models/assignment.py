from pydantic import BaseModel


class AssignmentField:
    OLD_INTERFACE_ID = "old_interface_id"
    CURRENT_INTERFACE_ID = "current_interface_id"
    USERNAME = "user_id"
    ASSIGN_BY = "assign_by"
    TYPE_STATUS = "type_status"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class AssignmentCompleteField:
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
    ASSIGN_BY = "assign_by"
    TYPE_STATUS = "type_status"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    

class StatisticsField:
    TOTAL_PENDING_TODAY = "total_pending_today"
    TOTAL_INSPECTED_TODAY = "total_inspected_today"
    TOTAL_REDISCOVERED_TODAY = "total_rediscovered_today"
    TOTAL_PENDING_MONTH = "total_pending_month"
    TOTAL_INSPECTED_MONTH = "total_inspected_month"
    TOTAL_REDISCOVERED_MONTH = "total_rediscovered_month"
    USERNAME = "username"
    NAME = "name"
    LASTNAME = "lastname"



class NewAssignmentModel(BaseModel):
    old_interface_id: int
    current_interface_id: int
    username: str
    assign_by: str
    type_status: str


class AssignmentModel(BaseModel):
    old_interface_id: int
    current_interface_id: int
    username: str
    assign_by: str
    type_status: str
    created_at: str
    updated_at: str | None


class AssignmentCompleteModel(BaseModel):
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
    username: str
    name: str
    lastname: str
    assign_by: str
    type_status: str
    created_at: str
    updated_at: str | None


class ReassignmentModel(BaseModel):
    old_interface_id: int
    current_interface_id: int
    old_username: str
    new_username: str
    assign_by: str


class UpdateAssignmentModel(BaseModel):
    old_interface_id: int
    current_interface_id: int
    username: str
    type_status: str


class StatisticsModel(BaseModel):
    total_pending_today: int
    total_inspected_today: int
    total_rediscovered_today: int
    total_pending_month: int
    total_inspected_month: int
    total_rediscovered_month: int
    username: str
    name: str
    lastname: str