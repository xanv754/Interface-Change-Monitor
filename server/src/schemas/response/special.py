from pydantic import BaseModel


class AssignmentsCountResponse(BaseModel):
    """Response of the total number of pending and revised assignments of an operator."""

    total_pending: int
    total_revised: int
