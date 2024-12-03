from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from database.constants.types.assignment import Status

class AssignmentField(Enum):
    changeInterface = "changeInterface"
    oldInterface = "oldInterface"
    operator = "operator"
    dateAssignment = "dateAssignment"
    statusAssignment = "statusAssignment"
    assignedBy = "assignedBy"
    dateReview = "dateReview"

class AssignmentEntity(BaseModel):
    changeInterface: int
    oldInterface: int
    operator: str
    dateAssignment: datetime
    statusAssignment: Status
    assignedBy: str
    dateReview: datetime | None