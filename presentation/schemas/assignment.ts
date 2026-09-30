import { z } from "zod";

export const newAssignmentSchema = z.object({
  old_interface_id: z.number(),
  current_interface_id: z.number(),
  username: z.string(),
  assign_by: z.string(),
  type_status: z.string(),
});

export type NewAssignmentSchema = z.infer<typeof newAssignmentSchema>;

export const reassignmentSchema = z.object({
  old_interface_id: z.number(),
  current_interface_id: z.number(),
  old_username: z.string(),
  new_username: z.string(),
  assign_by: z.string(),
});

export type ReassignmentSchema = z.infer<typeof reassignmentSchema>;

export const updateAssignmentSchema = z.object({
  old_interface_id: z.number(),
  current_interface_id: z.number(),
  type_status: z.string(),
});

export type UpdateAssignmentSchema = z.infer<typeof updateAssignmentSchema>;

export const statisticsAssignmentSchema = z.object({
  total_pending_today: z.number(),
  total_inspected_today: z.number(),
  total_rediscovered_today: z.number(),
  total_pending_month: z.number(),
  total_inspected_month: z.number(),
  total_rediscovered_month: z.number(),
  username: z.string(),
  name: z.string(),
  lastname: z.string(),
});

export type StatisticsAssignmentSchema = z.infer<typeof statisticsAssignmentSchema>;
