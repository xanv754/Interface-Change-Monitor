export interface InterfaceChangeSchema {
  id_old: number;
  ip_old: string;
  community_old: string;
  sysname_old: string;
  ifIndex_old: string;
  ifName_old: string;
  id_new: number;
  ifDescr_old: string;
  ifAlias_old: string;
  ifHighSpeed_old: string;
  ifOperStatus_old: string;
  ifAdminStatus_old: string;
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

export interface InterfaceAssignedSchema {
  id_old: number;
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
  id_new: number;
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
  username: string;
  name: string;
  lastname: string;
  assign_by: string;
  type_status: string;
  created_at: string;
  updated_at: string | null;
}
