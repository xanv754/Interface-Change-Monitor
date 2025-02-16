from pydantic import BaseModel


class TokenData(BaseModel):
    """Data of the token."""

    username: str
