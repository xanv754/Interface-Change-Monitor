from enum import Enum


class OperatorSchemaDB(Enum):
    """Names of the columns of the operator table."""

    USERNAME = "username"
    NAME = "name"
    LASTNAME = "lastname"
    PASSWORD = "password"
    PROFILE = "profile"
    STATUS_ACCOUNT = "statusaccount"
    CREATED_AT = "createdat"
