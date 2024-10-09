from models.assignment import AssignmentModel
from entity.interface import Interface
from pydantic import BaseModel

class Element(BaseModel):
    id: (str | None) = None
    date: str
    old: Interface
    current: Interface
    assignment: AssignmentModel
