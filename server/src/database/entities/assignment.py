from datetime import datetime
from pydantic import BaseModel
from database.constants.assignment import TypeStatusAssignment

class AssignmentEntity(BaseModel):
    idInterfaceToday: int
    idInterfaceYesterday: int
    operator: str
    dateAssignment: datetime
    statusAssignment: TypeStatusAssignment
    assignedBy: str
    dateReview: datetime | None