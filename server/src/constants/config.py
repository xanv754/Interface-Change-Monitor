"""This is the default configuration of the system."""
from schemas.json import JSONSettingSchema, JSONChangeNotificacionSchema, JSONUserPermission


DEFAULT = {
    f"{JSONSettingSchema.CAN_ASSING.value}": {
        f"{JSONUserPermission.ROOT.value}": True,
        f"{JSONUserPermission.ADMIN.value}": True,
        f"{JSONUserPermission.STANDARD.value}": False,
        f"{JSONUserPermission.SOPORT.value}": False
    },
    f"{JSONSettingSchema.CAN_RECEIVE_ASSIGNMENT.value}": {
        f"{JSONUserPermission.ROOT.value}": False,
        f"{JSONUserPermission.ADMIN.value}": True,
        f"{JSONUserPermission.STANDARD.value}": True,
        f"{JSONUserPermission.SOPORT.value}": False
    },
    f"{JSONSettingSchema.SYSTEM_INFORMATION.value}": {
        f"{JSONUserPermission.ROOT.value}": True,
        f"{JSONUserPermission.ADMIN.value}": True,
        f"{JSONUserPermission.STANDARD.value}": False,
        f"{JSONUserPermission.SOPORT.value}": True
    },
    f"{JSONSettingSchema.NOTIFICATION_CHANGES.value}": {
        f"{JSONChangeNotificacionSchema.IF_NAME.value}": True,
        f"{JSONChangeNotificacionSchema.IF_DESCR.value}": True,
        f"{JSONChangeNotificacionSchema.IF_ALIAS.value}": True,
        f"{JSONChangeNotificacionSchema.IF_HIGHSPEED.value}": True,
        f"{JSONChangeNotificacionSchema.IF_OPERSTATUS.value}": True,
        f"{JSONChangeNotificacionSchema.IF_ADMINSTATUS.value}": True,
    }
}
