from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Schema of the token."""

    access_token: str
    token_type: str
