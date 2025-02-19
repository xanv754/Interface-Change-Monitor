export interface ChangeSchema {
    ip: string;
    community: string;
    sysname: string;
    ifIndex: number;
    oldInteface: ChangeInterfaceSchema;
    newInteface: ChangeInterfaceSchema;
}

export interface ChangeInterfaceSchema {
    id: number;
    date: string;
    ifName: string;
    ifDescr: string;
    ifAlias: string;
    ifSpeed: number;
    ifHighSpeed: number;
    ifPhysAddress: string;
    ifType: string;
    ifOperStatus: string;
    ifAdminStatus: string;
    ifPromiscuousMode: boolean;
    ifConnectorPresent: boolean;
    ifLastChange: string;
}