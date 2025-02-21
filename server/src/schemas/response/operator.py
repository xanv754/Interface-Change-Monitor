from schemas import SystemConfigSchema
from pydantic import BaseModel

class OperatorResponseSchema(BaseModel):
    """Schema of the operator response."""

    username: str
    name: str
    lastname: str
    profile: str
    account: str
    createdAt: str
    configuration: SystemConfigSchema