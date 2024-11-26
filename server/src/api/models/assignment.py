from datetime import datetime
from pydantic import BaseModel

class AssignmentBodyModel(BaseModel):
    changeInterface: int
    oldInterface: int
    operator: str
    dateAssignment: datetime
    statusAssignment: str
    assignedBy: str
    dateReview: datetime