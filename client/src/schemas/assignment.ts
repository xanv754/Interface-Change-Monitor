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
    totalPending: number;
    totalRevised: number;
}