"""This is the default configuration of the system."""

from schemas import ConfigurationJsonSchema

DEFAULT = {
    f"{ConfigurationJsonSchema.CAN_ASSING.value}": {
        "ROOT": True,
        "ADMIN": True,
        "STANDARD": False,
        "SOPORT": False
    },
    f"{ConfigurationJsonSchema.CAN_RECEIVE_ASSIGNMENT.value}": {
        "ROOT": False,
        "ADMIN": True,
        "STANDARD": True,
        "SOPORT": False
    },
    f"{ConfigurationJsonSchema.SYSTEM_INFORMATION.value}": {
        "ROOT": True,
        "ADMIN": True,
        "STANDARD": False,
        "SOPORT": True
    },
    f"{ConfigurationJsonSchema.NOTIFICATION_CHANGES.value}": {
        "ifName": True,
        "ifDescr": True,
        "ifAlias": True,
        "ifHighSpeed": True,
        "ifOperStatus": True,
        "ifAdminStatus": True,
    }
}