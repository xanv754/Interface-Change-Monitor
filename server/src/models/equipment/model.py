from pydantic import BaseModel


class EquipmentModel(BaseModel):
    id: int | None
    ip: str
    community: str
    sysname: str
    createdat: str | None
    updatedat: str | None