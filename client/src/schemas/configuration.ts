export interface ConfigurationUserSchema {
    ROOT: boolean;
    ADMIN: boolean;
    STANDARD: boolean;
    SOPORT: boolean;
}

export interface ConfigurationNotificationSchema {
    ifName: boolean;
    ifDescr: boolean;
    ifAlias: boolean;
    ifHighSpeed: boolean;
    ifOperStatus: boolean;
    ifAdminStatus: boolean;
}

export interface ConfigurationResponseSchema {
    canAssign: ConfigurationUserSchema;
    canReceiveAssignment: ConfigurationUserSchema;
    systemInformation: ConfigurationUserSchema;
    notificationChanges: ConfigurationNotificationSchema;
}