from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Schema of the token."""

    accessToken: str
    typeToken: str
