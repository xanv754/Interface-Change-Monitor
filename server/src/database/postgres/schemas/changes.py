from enum import Enum


class ChangesSchemaDB(Enum):
    """Names of the columns of the changes table."""

    ID = "id"
    NEW_INTERFACE = "newinterface"
    OLD_INTERFACE = "oldinterface"
    OPERATOR = "operator"
