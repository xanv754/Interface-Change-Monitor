"""This is the default configuration of the system."""

from schemas import SystemConfigJson

DEFAULT = {
    f"{SystemConfigJson.CAN_ASSING.value}": {
        "ROOT": True,
        "ADMIN": True,
        "STANDARD": False,
        "SOPORT": False
    },
    f"{SystemConfigJson.CAN_RECEIVE_ASSIGNMENT.value}": {
        "ROOT": False,
        "ADMIN": True,
        "STANDARD": True,
        "SOPORT": False
    },
    f"{SystemConfigJson.SYSTEM_INFORMATION.value}": {
        "ROOT": True,
        "ADMIN": True,
        "STANDARD": False,
        "SOPORT": True
    },
    f"{SystemConfigJson.NOTIFICATION_CHANGES.value}": {
        "ifName": True,
        "ifDescr": True,
        "ifAlias": True,
        "ifHighSpeed": True,
        "ifOperStatus": True,
        "ifAdminStatus": True,
    }
}