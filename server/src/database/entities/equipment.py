from enum import Enum
from datetime import datetime
from pydantic import BaseModel

class EquipmentField(Enum):
    id = "id"
    ip = "ip"
    community = "community"
    sysname = "sysname"
    createdAt = "createdAt"
    updatedAt = "updatedAt"

class EquipmentEntity(BaseModel):
    id: int
    ip: str
    community: str
    sysname: str
    createdAt: datetime
    updatedAt: datetime | None