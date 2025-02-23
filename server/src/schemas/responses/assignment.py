from pydantic import BaseModel


class StatisticsAssignmentResponse(BaseModel):
    """Response of the total number of pending and revised assignments of an operator."""

    username: str
    name: str
    lastname: str
    totalPending: int
    totalRevised: int
