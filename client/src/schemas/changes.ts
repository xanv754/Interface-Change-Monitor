export interface ChangeResponseSchema {
    id: number;
    ip: string;
    community: string;
    sysname: string;
    ifIndex: number;
    oldInterface: ChangeInterfaceSchema;
    newInterface: ChangeInterfaceSchema;
    operator: string | null;
}

export interface ChangeInterfaceSchema {
    id: number;
    equipment: number;
    date: string;
    type: string;
    ifName: string;
    ifDescr: string;
    ifAlias: string;
    ifHighSpeed: number;
    ifOperStatus: string;
    ifAdminStatus: string;
}