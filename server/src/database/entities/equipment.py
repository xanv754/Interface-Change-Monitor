from datetime import datetime
from pydantic import BaseModel

class EquipmentEntity(BaseModel):
    id: int
    ip: str
    community: str
    sysname: str
    createdAt: datetime
    updatedAt: datetime | None