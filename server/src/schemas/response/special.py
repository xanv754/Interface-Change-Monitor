from pydantic import BaseModel


class AssignmentsCountResponse(BaseModel):
    total_pending: int
    total_revised: int