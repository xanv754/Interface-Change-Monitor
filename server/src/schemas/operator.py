from pydantic import BaseModel
from schemas.config import SettingSchema

class OperatorSchema(BaseModel):
    """Schema of the operator in the database."""

    username: str
    name: str
    lastname: str
    password: str
    profile: str
    account: str
    createdAt: str

class UserSchema(BaseModel):
    """Schema of the an user."""

    username: str
    name: str
    lastname: str
    profile: str
    account: str
    createdAt: str
    configuration: SettingSchema


class UpdatePasswordBody(BaseModel):
    """Attributes necessary to update the password of an operator."""

    password: str


class UpdateProfileBody(BaseModel):
    """Attributes necessary to update the profile of an operator."""

    username: str
    profile: str


class UpdateAccountBody(BaseModel):
    """Attributes necessary to update the account of an operator."""

    username: str
    account: str


class UpdateUserRootBody(BaseModel):
    """Attributes necessary to update an operator."""

    username: str
    name: str
    lastname: str
    profile: str
    account: str


class UpdateUserStandardBody(BaseModel):
    """Attributes necessary to update an operator in standard profile."""

    name: str
    lastname: str


class RegisterUserBody(BaseModel):
    """Attributes necessary to register an operator."""

    username: str
    name: str
    lastname: str
    password: str
    profile: str
