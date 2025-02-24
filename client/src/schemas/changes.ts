export interface ChangeResponseSchema {
    ip: string;
    community: string;
    sysname: string;
    ifIndex: number;
    oldInterface: ChangeInterfaceSchema;
    newInterface: ChangeInterfaceSchema;
}

export interface ChangeInterfaceSchema {
    id: number;
    date: string;
    ifName: string;
    ifDescr: string;
    ifAlias: string;
    ifHighSpeed: number;
    ifOperStatus: string;
    ifAdminStatus: string;
}