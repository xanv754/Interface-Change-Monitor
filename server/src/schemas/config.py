from pydantic import BaseModel


class ConfigUserSchema(BaseModel):
    """Schema of the settings of the user."""
    ROOT: bool
    ADMIN: bool
    STANDARD: bool
    SOPORT: bool


class ConfigNotificationSchema(BaseModel):
    """Schema of the settings of the notifications."""
    ifName: bool
    ifDescr: bool
    ifAlias: bool
    ifHighSpeed: bool
    ifOperStatus: bool
    ifAdminStatus: bool


class ConfigurationSchema(BaseModel):
    """Schema of the settings of the system."""
    canAssign: ConfigUserSchema
    canReceiveAssignment: ConfigUserSchema
    systemInformation: ConfigUserSchema
    notificationChanges: ConfigNotificationSchema