from pydantic import BaseModel


class EquipmentSchema(BaseModel):
    """Schema of the equipment."""

    id: int
    ip: str
    community: str
    sysname: str | None
    created_at: str
    updated_at: str | None
