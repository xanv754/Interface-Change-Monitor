from enum import Enum
from constants.types import ProfileType


class JSONUserPermission(Enum):
    """JSON of the settings of user permissions."""

    ROOT = ProfileType.ROOT.value
    ADMIN = ProfileType.ADMIN.value
    STANDARD = ProfileType.STANDARD.value
    SOPORT = ProfileType.SOPORT.value


class JSONChangeNotificacionSchema(Enum):
    """JSON of the settings of the notifications."""

    IF_NAME = "ifName"
    IF_DESCR = "ifDescr"
    IF_ALIAS = "ifAlias"
    IF_HIGHSPEED = "ifHighSpeed"
    IF_OPERSTATUS = "ifOperStatus"
    IF_ADMINSTATUS = "ifAdminStatus"


class JSONSettingSchema(Enum):
    """JSON of the settings of the system."""

    CAN_ASSING = "canAssign"
    CAN_RECEIVE_ASSIGNMENT = "canReceiveAssignment"
    SYSTEM_INFORMATION = "systemInformation"
    NOTIFICATION_CHANGES = "notificationChanges"
