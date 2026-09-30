import { z } from "zod";

export const interfaceChangeSchema = z.object({
  id_old: z.number(),
  ip_old: z.string(),
  community_old: z.string(),
  sysname_old: z.string(),
  ifIndex_old: z.string(),
  ifName_old: z.string(),
  id_new: z.number(),
  ifDescr_old: z.string(),
  ifAlias_old: z.string(),
  ifHighSpeed_old: z.string(),
  ifOperStatus_old: z.string(),
  ifAdminStatus_old: z.string(),
  ip_new: z.string(),
  community_new: z.string(),
  sysname_new: z.string(),
  ifIndex_new: z.string(),
  ifName_new: z.string(),
  ifDescr_new: z.string(),
  ifAlias_new: z.string(),
  ifHighSpeed_new: z.string(),
  ifOperStatus_new: z.string(),
  ifAdminStatus_new: z.string(),
  username: z.string().nullable(),
  name: z.string().nullable(),
  lastname: z.string().nullable(),
});

export type InterfaceChangeSchema = z.infer<typeof interfaceChangeSchema>;

export const interfaceAssignedSchema = z.object({
  id_old: z.number(),
  ip_old: z.string(),
  community_old: z.string(),
  sysname_old: z.string(),
  ifIndex_old: z.string(),
  ifName_old: z.string(),
  ifDescr_old: z.string(),
  ifAlias_old: z.string(),
  ifHighSpeed_old: z.string(),
  ifOperStatus_old: z.string(),
  ifAdminStatus_old: z.string(),
  id_new: z.number(),
  ip_new: z.string(),
  community_new: z.string(),
  sysname_new: z.string(),
  ifIndex_new: z.string(),
  ifName_new: z.string(),
  ifDescr_new: z.string(),
  ifAlias_new: z.string(),
  ifHighSpeed_new: z.string(),
  ifOperStatus_new: z.string(),
  ifAdminStatus_new: z.string(),
  username: z.string(),
  name: z.string(),
  lastname: z.string(),
  assign_by: z.string(),
  type_status: z.string(),
  created_at: z.string(),
  updated_at: z.string().nullable(),
});

export type InterfaceAssignedSchema = z.infer<typeof interfaceAssignedSchema>;

export const paginatedChangesSchema = z.object({
  items: z.array(interfaceChangeSchema),
  total: z.number(),
  page: z.number(),
  page_size: z.number(),
  total_pages: z.number(),
});

export type PaginatedChangesSchema = z.infer<typeof paginatedChangesSchema>;
