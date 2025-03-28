from pydantic import BaseModel
from schemas.interface import InterfaceSchema


class ChangeSchema(BaseModel):
    """Schema of the a change in the database."""

    id: int
    newInterface: int
    oldInterface: int
    operator: str | None


class ChangeInterfaceSchema(BaseModel):
    """Schema of the an change with all information of the interface."""

    id: int
    ip: str
    community: str
    sysname: str
    ifIndex: int
    oldInterface: InterfaceSchema
    newInterface: InterfaceSchema
    operator: str | None


class RegisterChangeBody(BaseModel):
    """Attributes necessary to register an change."""

    newInterface: int
    oldInterface: int
