from datetime import datetime
from pydantic import BaseModel
from database.constants.assignment import TypeStatusAssignment

class AssignmentEntity(BaseModel):
    changeInterface: int
    oldInterface: int
    operator: str
    dateAssignment: datetime
    statusAssignment: TypeStatusAssignment
    assignedBy: str
    dateReview: datetime | None