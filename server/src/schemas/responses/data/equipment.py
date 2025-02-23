from pydantic import BaseModel


class EquipmentResponseSchema(BaseModel):
    """Schema of the equipment."""

    id: int
    ip: str
    community: str
    sysname: str | None
    createdAt: str
    updatedAt: str | None
