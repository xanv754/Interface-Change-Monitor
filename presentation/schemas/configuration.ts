export interface UserConfigurationSchema {
    root: boolean;
    admin: boolean;
    user: boolean;
    soport: boolean;
}

export interface NotificationConfigurationSchema {
    ifName: boolean;
    ifDescr: boolean;
    ifAlias: boolean;
    ifHighSpeed: boolean;
    ifOperStatus: boolean;
    ifAdminStatus: boolean;
}

export interface ConfigurationSchema {
    can_assign: UserConfigurationSchema;
    can_receive_assignment: UserConfigurationSchema;
    view_information_global: UserConfigurationSchema;
    notifications: NotificationConfigurationSchema;
}