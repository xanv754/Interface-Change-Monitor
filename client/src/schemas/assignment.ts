export interface AssignmentResponseSchema {
    id: number;
    idNewInterface: number;
    idOldInterface: number;
    operator: string;
    date: string;
    status: string;
    assignedBy: string;
    updatedAt: string;
}

export interface AssignmentInfoResponseSchema {
    idAssignment: number;
    dateAssignment: string;
    statusAssignment: string;
    assignedBy: string;
    updateAt: string;
    oldIfName: string;
    oldIfDescr: string;
    oldIfAlias: string;
    oldIfHighSpeed: number;
    oldIfOperStatus: string;
    oldIfAdminStatus: string;
    newIfName: string;
    newIfDescr: string;
    newIfAlias: string;
    newIfHighSpeed: number;
    newIfOperStatus: string;
    newIfAdminStatus: string;
    ip: string;
    community: string;
    sysname: string;
    ifIndex: number;
}

export interface AssignmentStatisticsResponseSchema {
    username: string;
    name: string;
    lastname: string;
    totalPending: number;
    totalRevised: number;
}

export interface AssignmentUpdateStatusRequestSchema {
    idAssignment: number;
    newStatus: string;
}

export interface AssignRequestSchema {
    newInterface: number;
    oldInterface: number;
    operator: string;
    assignedBy: string;
}

export interface ReassingRequestSchema {
    idAssignment: number;
    newOperator: string;
    assignedBy: string;
}