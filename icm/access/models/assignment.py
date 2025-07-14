from pydantic import BaseModel


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