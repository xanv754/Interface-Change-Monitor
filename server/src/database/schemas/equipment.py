from enum import Enum


class EquipmentSchemaDB(Enum):
    """Names of the columns of the equipment table."""

    ID = "id"
    IP = "ip"
    COMMUNITY = "community"
    SYSNAME = "sysname"
    CREATED_AT = "createdat"
    UPDATED_AT = "updatedat"
