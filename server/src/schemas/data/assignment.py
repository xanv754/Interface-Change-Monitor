from pydantic import BaseModel


class AssignmentSchema(BaseModel):
    id: int
    new_interface: int
    old_interface: int
    operator: str
    date: str
    status: str
    assigned_by: str
    updated_at: str | None