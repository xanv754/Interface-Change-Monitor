from schemas import SystemConfigSchema, SystemConfigUserSchema, SystemConfigNotificationSchema

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
        "ifSpeed": False,
        "ifHighSpeed": True,
        "ifPhysAddress": False,
        "ifType": False,
        "ifOperStatus": True,
        "ifAdminStatus": True,
        "ifPromiscuousMode": False,
        "ifConnectorPresent": False,
        "ifLastCheck": False
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
        "ifSpeed": False,
        "ifHighSpeed": False,
        "ifPhysAddress": False,
        "ifType": False,
        "ifOperStatus": False,
        "ifAdminStatus": False,
        "ifPromiscuousMode": False,
        "ifConnectorPresent": False,
        "ifLastCheck": False
    }
}

DEFAULT_OBJECT = SystemConfigSchema(
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
        ifSpeed=False,
        ifHighSpeed=True,
        ifPhysAddress=False,
        ifType=False,
        ifOperStatus=True,
        ifAdminStatus=True,
        ifPromiscuousMode=False,
        ifConnectorPresent=False,
        ifLastCheck=False
    )
)

ALTERNATIVE_OBJECT = SystemConfigSchema(
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
        ifSpeed=False,
        ifHighSpeed=False,
        ifPhysAddress=False,
        ifType=False,
        ifOperStatus=False,
        ifAdminStatus=False,
        ifPromiscuousMode=False,
        ifConnectorPresent=False,
        ifLastCheck=False
    )
)