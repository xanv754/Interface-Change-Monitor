import { z } from "zod";

export const userConfigurationSchema = z.object({
  root: z.boolean(),
  admin: z.boolean(),
  user: z.boolean(),
  soport: z.boolean(),
});

export type UserConfigurationSchema = z.infer<typeof userConfigurationSchema>;

export const notificationConfigurationSchema = z.object({
  ifName: z.boolean(),
  ifDescr: z.boolean(),
  ifAlias: z.boolean(),
  ifHighSpeed: z.boolean(),
  ifOperStatus: z.boolean(),
  ifAdminStatus: z.boolean(),
});

export type NotificationConfigurationSchema = z.infer<typeof notificationConfigurationSchema>;

export const configurationSchema = z.object({
  can_assign: userConfigurationSchema,
  can_receive_assignment: userConfigurationSchema,
  notification_changes: notificationConfigurationSchema,
  view_information_global: userConfigurationSchema,
});

export type ConfigurationSchema = z.infer<typeof configurationSchema>;
