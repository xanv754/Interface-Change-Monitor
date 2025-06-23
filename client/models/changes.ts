export interface ChangeInterface {
    id_old: string;
    ip_old: string;
    community_old: string;
    sysname_old: string;
    ifIndex_old: string;
    ifName_old: string;
    ifDescr_old: string;
    ifAlias_old: string;
    ifHighSpeed_old: string;
    ifOperStatus_old: string;
    ifAdminStatus_old: string;
    id_new: string;
    ip_new: string;
    community_new: string;
    sysname_new: string;
    ifIndex_new: string;
    ifName_new: string;
    ifDescr_new: string;
    ifAlias_new: string;
    ifHighSpeed_new: string;
    ifOperStatus_new: string;
    ifAdminStatus_new: string;
    username: string | null;
    name: string | null;
    lastname: string | null;
}