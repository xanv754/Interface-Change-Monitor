"""This is the default configuration of the system."""

from schemas import JSONSettingSchema

DEFAULT = {
    f"{JSONSettingSchema.CAN_ASSING.value}": {
        "ROOT": True,
        "ADMIN": True,
        "STANDARD": False,
        "SOPORT": False
    },
    f"{JSONSettingSchema.CAN_RECEIVE_ASSIGNMENT.value}": {
        "ROOT": False,
        "ADMIN": True,
        "STANDARD": True,
        "SOPORT": False
    },
    f"{JSONSettingSchema.SYSTEM_INFORMATION.value}": {
        "ROOT": True,
        "ADMIN": True,
        "STANDARD": False,
        "SOPORT": True
    },
    f"{JSONSettingSchema.NOTIFICATION_CHANGES.value}": {
        "ifName": True,
        "ifDescr": True,
        "ifAlias": True,
        "ifHighSpeed": True,
        "ifOperStatus": True,
        "ifAdminStatus": True,
    }
}