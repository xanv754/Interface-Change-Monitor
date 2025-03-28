from pydantic import BaseModel


class UserPermissionSchema(BaseModel):
    """Schema of permissions settings of the user."""

    ROOT: bool
    ADMIN: bool
    STANDARD: bool
    SOPORT: bool


class ChangeNotificationSchema(BaseModel):
    """Schema of the settings of the notifications."""

    ifName: bool
    ifDescr: bool
    ifAlias: bool
    ifHighSpeed: bool
    ifOperStatus: bool
    ifAdminStatus: bool


class SettingSchema(BaseModel):
    """Schema of the settings of the system."""

    canAssign: UserPermissionSchema
    canReceiveAssignment: UserPermissionSchema
    systemInformation: UserPermissionSchema
    notificationChanges: ChangeNotificationSchema
