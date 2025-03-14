from schemas import ConfigurationSchema, ConfigUserSchema, ConfigNotificationSchema, ConfigurationJsonSchema

DEFAULT_DICT = {
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

ALTERNATIVE_DICT = {
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
        "ifName": False,
        "ifDescr": False,
        "ifAlias": False,
        "ifHighSpeed": False,
        "ifOperStatus": False,
        "ifAdminStatus": False,
    }
}

DEFAULT_OBJECT = ConfigurationSchema(
    canAssign=ConfigUserSchema(
        ROOT=True,
        ADMIN=True,
        STANDARD=False,
        SOPORT=False
    ),
    canReceiveAssignment=ConfigUserSchema(
        ROOT=False,
        ADMIN=True,
        STANDARD=True,
        SOPORT=False
    ),
    systemInformation=ConfigUserSchema(
        ROOT=True,
        ADMIN=True,
        STANDARD=False,
        SOPORT=True
    ),
    notificationChanges=ConfigNotificationSchema(
        ifName=True,
        ifDescr=True,
        ifAlias=True,
        ifHighSpeed=True,
        ifOperStatus=True,
        ifAdminStatus=True,
    )
)

ALTERNATIVE_OBJECT = ConfigurationSchema(
    canAssign=ConfigUserSchema(
        ROOT=True,
        ADMIN=True,
        STANDARD=False,
        SOPORT=False
    ),
    canReceiveAssignment=ConfigUserSchema(
        ROOT=False,
        ADMIN=True,
        STANDARD=True,
        SOPORT=False
    ),
    systemInformation=ConfigUserSchema(
        ROOT=True,
        ADMIN=True,
        STANDARD=False,
        SOPORT=True
    ),
    notificationChanges=ConfigNotificationSchema(
        ifName=False,
        ifDescr=False,
        ifAlias=False,
        ifHighSpeed=False,
        ifOperStatus=False,
        ifAdminStatus=False,
    )
)
