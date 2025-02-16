from pydantic import BaseModel


class Token(BaseModel):
    """Schema of the token."""

    access_token: str
    token_type: str
