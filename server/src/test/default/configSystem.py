from schemas import SystemConfigResponse, SystemConfigUserSchema, SystemConfigNotificationSchema, SystemConfigJson

DEFAULT_DICT = {
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

ALTERNATIVE_DICT = {
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
        "ifName": False,
        "ifDescr": False,
        "ifAlias": False,
        "ifHighSpeed": False,
        "ifOperStatus": False,
        "ifAdminStatus": False,
    }
}

DEFAULT_OBJECT = SystemConfigResponse(
    canAssign=SystemConfigUserSchema(
        ROOT=True,
        ADMIN=True,
        STANDARD=False,
        SOPORT=False
    ),
    canReceiveAssignment=SystemConfigUserSchema(
        ROOT=False,
        ADMIN=True,
        STANDARD=True,
        SOPORT=False
    ),
    systemInformation=SystemConfigUserSchema(
        ROOT=True,
        ADMIN=True,
        STANDARD=False,
        SOPORT=True
    ),
    notificationChanges=SystemConfigNotificationSchema(
        ifName=True,
        ifDescr=True,
        ifAlias=True,
        ifHighSpeed=True,
        ifOperStatus=True,
        ifAdminStatus=True,
    )
)

ALTERNATIVE_OBJECT = SystemConfigResponse(
    canAssign=SystemConfigUserSchema(
        ROOT=True,
        ADMIN=True,
        STANDARD=False,
        SOPORT=False
    ),
    canReceiveAssignment=SystemConfigUserSchema(
        ROOT=False,
        ADMIN=True,
        STANDARD=True,
        SOPORT=False
    ),
    systemInformation=SystemConfigUserSchema(
        ROOT=True,
        ADMIN=True,
        STANDARD=False,
        SOPORT=True
    ),
    notificationChanges=SystemConfigNotificationSchema(
        ifName=False,
        ifDescr=False,
        ifAlias=False,
        ifHighSpeed=False,
        ifOperStatus=False,
        ifAdminStatus=False,
    )
)
