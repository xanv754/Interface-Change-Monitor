from pydantic import BaseModel

class AssigmentStatusModel(BaseModel):
    username: str
    idElement: str
    status: str   