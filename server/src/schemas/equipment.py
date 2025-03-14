from pydantic import BaseModel


class EquipmentSchema(BaseModel):
    """Basic schema of the equipment."""

    id: int
    ip: str
    community: str
    sysname: str | None
    createdAt: str
    updatedAt: str | None


class RegisterEquipmentBody(BaseModel):
    """Attributes necessary to register an equipment."""

    ip: str
    community: str
    sysname: str | None = None