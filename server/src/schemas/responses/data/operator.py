from pydantic import BaseModel


class OperatorResponseSchema(BaseModel):
    """Schema of the operator."""

    username: str
    name: str
    lastname: str
    password: str
    profile: str
    account: str
    createdAt: str
