from pydantic import BaseModel


class UpdateChangeModel(BaseModel):
    id_old: int
    id_new: int
    username: str