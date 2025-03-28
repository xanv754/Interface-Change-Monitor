from schemas import SettingSchema, UserPermissionSchema, ChangeNotificationSchema, JSONSettingSchema

DEFAULT_DICT = {
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

ALTERNATIVE_DICT = {
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
        "ifName": False,
        "ifDescr": False,
        "ifAlias": False,
        "ifHighSpeed": False,
        "ifOperStatus": False,
        "ifAdminStatus": False,
    }
}

DEFAULT_OBJECT = SettingSchema(
    canAssign=UserPermissionSchema(
        ROOT=True,
        ADMIN=True,
        STANDARD=False,
        SOPORT=False
    ),
    canReceiveAssignment=UserPermissionSchema(
        ROOT=False,
        ADMIN=True,
        STANDARD=True,
        SOPORT=False
    ),
    systemInformation=UserPermissionSchema(
        ROOT=True,
        ADMIN=True,
        STANDARD=False,
        SOPORT=True
    ),
    notificationChanges=ChangeNotificationSchema(
        ifName=True,
        ifDescr=True,
        ifAlias=True,
        ifHighSpeed=True,
        ifOperStatus=True,
        ifAdminStatus=True,
    )
)

ALTERNATIVE_OBJECT = SettingSchema(
    canAssign=UserPermissionSchema(
        ROOT=True,
        ADMIN=True,
        STANDARD=False,
        SOPORT=False
    ),
    canReceiveAssignment=UserPermissionSchema(
        ROOT=False,
        ADMIN=True,
        STANDARD=True,
        SOPORT=False
    ),
    systemInformation=UserPermissionSchema(
        ROOT=True,
        ADMIN=True,
        STANDARD=False,
        SOPORT=True
    ),
    notificationChanges=ChangeNotificationSchema(
        ifName=False,
        ifDescr=False,
        ifAlias=False,
        ifHighSpeed=False,
        ifOperStatus=False,
        ifAdminStatus=False,
    )
)
