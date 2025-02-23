from schemas import SystemConfigResponse, SystemConfigUserSchema, SystemConfigNotificationSchema

DEFAULT_DICT = {
    "canAssign": {
        "ROOT": True,
        "ADMIN": True,
        "STANDARD": False,
        "SOPORT": False
    },
    "canReceiveAssignment": {
        "ROOT": False,
        "ADMIN": True,
        "STANDARD": True,
        "SOPORT": False
    },
    "viewAllStatistics": {
        "ROOT": True,
        "ADMIN": True,
        "STANDARD": False,
        "SOPORT": True
    },
    "notificationChanges": {
        "ifName": True,
        "ifDescr": True,
        "ifAlias": True,
        "ifHighSpeed": True,
        "ifOperStatus": True,
        "ifAdminStatus": True,
    }
}

ALTERNATIVE_DICT = {
    "canAssign": {
        "ROOT": True,
        "ADMIN": True,
        "STANDARD": False,
        "SOPORT": False
    },
    "canReceiveAssignment": {
        "ROOT": False,
        "ADMIN": True,
        "STANDARD": True,
        "SOPORT": False
    },
    "viewAllStatistics": {
        "ROOT": True,
        "ADMIN": True,
        "STANDARD": False,
        "SOPORT": True
    },
    "notificationChanges": {
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
    viewAllStatistics=SystemConfigUserSchema(
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
    viewAllStatistics=SystemConfigUserSchema(
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
