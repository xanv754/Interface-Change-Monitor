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
    ifSpeed: boolean;
    ifHighSpeed: boolean;
    ifPhysAddress: boolean;
    ifType: boolean;
    ifOperStatus: boolean;
    ifAdminStatus: boolean;
    ifPromiscuousMode: boolean;
    ifConnectorPresent: boolean;
    ifLastChange: boolean;
}

export interface ConfigurationSchema {
    canAssign: ConfigurationUserSchema;
    canReceiveAssignment: ConfigurationUserSchema;
    viewAllStatistics: ConfigurationUserSchema;
    notificationChanges: ConfigurationNotificationSchema;
}