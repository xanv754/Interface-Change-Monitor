from pydantic import BaseModel


class NewAssignmentModel(BaseModel):
    old_interface_id: int
    current_interface_id: int
    username: str
    assign_by: str
    type_status: str


class AssignmentModel(BaseModel):
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