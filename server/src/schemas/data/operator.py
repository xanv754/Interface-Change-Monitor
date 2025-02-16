from pydantic import BaseModel


class OperatorSchema(BaseModel):
    """Schema of the operator."""

    username: str
    name: str
    lastname: str
    password: str
    profile: str
    account: str
    created_at: str
