export interface AssignmentSchema {
    id: number;
    idNewInterface: number;
    idOldInterface: number;
    operator: string;
    date: string;
    status: string;
    assignedBy: string;
    updatedAt: string;
}

export interface AssignmentInterfaceSchema {
    idAssignment: number;
    dateAssignment: string;
    statusAssignment: string;
    assignedBy: string;
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

export interface AssignmentBodyRegisterSchema {
    newInterface: number;
    oldInterface: number;
    operator: string;
    assignedBy: string;
}

export interface ReassignmentBodySchema {
    idAssignment: number;
    newOperator: string;
    assignedBy: string;
}

export interface AssignmentUpdateBodySchema {
    idAssignment: number;
    newStatus: string;
}

export interface AssignmentsTotalSchema {
    username: string;
    name: string;
    lastname: string;
    totalPending: number;
    totalRevised: number;
}