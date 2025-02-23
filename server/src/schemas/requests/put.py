from pydantic import BaseModel


class OperatorUpdateBody(BaseModel):
    """Attributes necessary to update an operator."""

    username: str
    name: str
    lastname: str
    profile: str
    account: str


class OperatorUpdateStandardBody(BaseModel):
    """Attributes necessary to update an operator in standard profile."""

    name: str
    lastname: str
