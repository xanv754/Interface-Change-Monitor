from enum import Enum


class ConfigNotificationJsonSchema(Enum):
    """JSON of the settings of the notifications."""

    IF_NAME = "ifName"
    IF_DESCR = "ifDescr"
    IF_ALIAS = "ifAlias"
    IF_HIGHSPEED = "ifHighSpeed"
    IF_OPERSTATUS = "ifOperStatus"
    IF_ADMINSTATUS = "ifAdminStatus"


class ConfigurationJsonSchema(Enum):
    """JSON of the settings of the system."""

    CAN_ASSING = "canAssign"
    CAN_RECEIVE_ASSIGNMENT = "canReceiveAssignment"
    SYSTEM_INFORMATION = "systemInformation"
    NOTIFICATION_CHANGES = "notificationChanges"


class ChangeJsonSchema(Enum):
    """JSON of the changes."""
    ID = "id"
    CHANGES = "changes"
