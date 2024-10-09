from models.assignment import AssignmentModel
from pydantic import BaseModel

class InterfaceModel(BaseModel):
    idElement: str
    ip: str
    community: str
    assignment: AssignmentModel