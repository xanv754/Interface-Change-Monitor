from pydantic import BaseModel


class SystemConfigUserSchema(BaseModel):
    """Schema of the settings of the user."""
    ROOT: bool
    ADMIN: bool
    STANDARD: bool
    SOPORT: bool


class SystemConfigNotificationSchema(BaseModel):
    """Schema of the settings of the notifications."""
    ifName: bool
    ifDescr: bool
    ifAlias: bool
    ifHighSpeed: bool
    ifOperStatus: bool
    ifAdminStatus: bool


class SystemConfigResponse(BaseModel):
    """Schema of the settings of the system."""
    canAssign: SystemConfigUserSchema
    canReceiveAssignment: SystemConfigUserSchema
    viewAllStatistics: SystemConfigUserSchema
    notificationChanges: SystemConfigNotificationSchema
