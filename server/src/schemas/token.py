from pydantic import BaseModel


class TokenDataSchema(BaseModel):
    """Data of the token."""

    username: str

class TokenResponseSchema(BaseModel):
    """Schema of the token."""

    access_token: str
    token_type: str