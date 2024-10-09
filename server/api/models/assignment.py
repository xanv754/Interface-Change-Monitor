from constants.assigmentStatus import assignmentstatus
from pydantic import BaseModel

class AssignmentModel(BaseModel):
    isAssigned: str = "false"
    assignedDate: (str | None) = None
    usernameAssigned: (str | None) = None
    status: str = assignmentstatus.default
    reviewDay: (str | None) = None
    reviewMonth: (str | None) = None
    reviewYear: (str | None) = None