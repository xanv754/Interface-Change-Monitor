from schemas import SystemConfigResponse
from pydantic import BaseModel

class OperatorResponse(BaseModel):
    """Schema of the operator response."""

    username: str
    name: str
    lastname: str
    profile: str
    account: str
    createdAt: str
    configuration: SystemConfigResponse