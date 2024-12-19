from enum import Enum
from datetime import datetime
from pydantic import BaseModel

class EquipmentEntity(BaseModel):
    id: int
    ip: str
    community: str
    sysname: str
    createdat: datetime | None
    updatedat: datetime | None

class EquipmentField(Enum):
    id = "id"
    ip = "ip"
    community = "community"
    sysname = "sysname"
    createdAt = "createdat"
    updatedAt = "updatedat"
