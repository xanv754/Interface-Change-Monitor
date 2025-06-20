export interface NewAssignmentModel {
    old_interface_id: number;
    current_interface_id: number;
    username: string;
    assign_by: string;
    type_status: string;
}


export interface AssignmentModel {
    old_interface_id: number;
    current_interface_id: number;
    username: string;
    assign_by: string;
    type_status: string;
    created_at: string;
    updated_at: string | null;
}