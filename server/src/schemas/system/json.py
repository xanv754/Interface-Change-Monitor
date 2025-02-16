from enum import Enum


class SystemConfigNotificationJson(Enum):
    """JSON of the settings of the notifications."""
    
    IF_NAME = "ifName"
    IF_DESCR = "ifDescr"
    IF_ALIAS = "ifAlias"
    IF_SPEED = "ifSpeed"
    IF_HIGHSPEED = "ifHighSpeed"
    IF_PHYSADDRESS = "ifPhysAddress"
    IF_TYPE = "ifType"
    IF_OPERSTATUS = "ifOperStatus"
    IF_ADMINSTATUS = "ifAdminStatus"
    IF_PROMISCUOUSMODE = "ifPromiscuousMode"
    IF_CONNECTORPRESENT = "ifConnectorPresent"
    IF_LASTCHECK = "ifLastCheck"


class SystemConfigJson(Enum):
    """JSON of the settings of the system."""
    
    CAN_ASSING = "canAssign"
    CAN_RECEIVE_ASSIGNMENT = "canReceiveAssignment"
    VIEW_ALL_STATISTICS = "viewAllStatistics"
    NOTIFICATION_CHANGES = "notificationChanges"