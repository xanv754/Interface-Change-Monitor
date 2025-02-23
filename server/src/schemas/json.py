from enum import Enum


class SystemConfigNotificationJson(Enum):
    """JSON of the settings of the notifications."""

    IF_NAME = "ifName"
    IF_DESCR = "ifDescr"
    IF_ALIAS = "ifAlias"
    IF_HIGHSPEED = "ifHighSpeed"
    IF_OPERSTATUS = "ifOperStatus"
    IF_ADMINSTATUS = "ifAdminStatus"


class SystemConfigJson(Enum):
    """JSON of the settings of the system."""

    CAN_ASSING = "canAssign"
    CAN_RECEIVE_ASSIGNMENT = "canReceiveAssignment"
    VIEW_ALL_STATISTICS = "viewAllStatistics"
    NOTIFICATION_CHANGES = "notificationChanges"


class ChangesJson(Enum):
    """JSON of the changes."""
    ID = "id"
    CHANGES = "changes"
