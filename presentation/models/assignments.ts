export interface NewAssignmentModel {
    old_interface_id: number;
    current_interface_id: number;
    username: string;
    assign_by: string;
    type_status: string;
}


export interface AssignmentBasicModel {
    old_interface_id: number;
    current_interface_id: number;
    username: string;
    assign_by: string;
    type_status: string;
    created_at: string;
    updated_at: string | null;
}

export interface AssignmentModel {
    id_old: number
    ip_old: string
    community_old: string
    sysname_old: string
    ifIndex_old: number
    ifName_old: string
    ifDescr_old: string
    ifAlias_old: string
    ifHighSpeed_old: number
    ifOperStatus_old: string
    ifAdminStatus_old: string
    id_new: number
    ip_new: string
    community_new: string
    sysname_new: string
    ifIndex_new: number
    ifName_new: string
    ifDescr_new: string
    ifAlias_new: string
    ifHighSpeed_new: number
    ifOperStatus_new: string
    ifAdminStatus_new: string
    username: string
    name: string
    lastname: string
    assign_by: string
    type_status: string
    created_at: string
    updated_at: string | null
}