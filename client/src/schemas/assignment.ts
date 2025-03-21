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
    username: string | null;
    name: string | null;
    lastname: string | null;
}

export interface AssignmentStatisticsOperatorsResponseSchema {
    username: string;
    name: string;
    lastname: string;
    totalPending: number;
    totalRevised: number;
}

export interface AssignmentStatisticsResponseSchema {
    totalPending: number;
    totalRevised: number;
}

export interface AssignmentUpdateStatusRequestSchema {
    idAssignment: number;
    newStatus: string;
}

export interface AssignRequestSchema {
    idChange: number;
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

export interface AutoAssignmentRequestSchema {
    users: string[];
    assignedBy: string;
}