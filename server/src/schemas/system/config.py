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
    ifSpeed: bool
    ifHighSpeed: bool
    ifPhysAddress: bool
    ifType: bool
    ifOperStatus: bool
    ifAdminStatus: bool
    ifPromiscuousMode: bool
    ifConnectorPresent: bool
    ifLastCheck: bool


class SystemConfigSchema(BaseModel):
    """Schema of the settings of the system."""
    canAssign: SystemConfigUserSchema
    canReceiveAssignment: SystemConfigUserSchema
    viewAllStatistics: SystemConfigUserSchema
    notificationChanges: SystemConfigNotificationSchema