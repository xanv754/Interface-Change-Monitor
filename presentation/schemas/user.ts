import { z } from "zod";

export const sessionSchema = z.object({
  username: z.string(),
  name: z.string(),
  lastname: z.string(),
  status: z.string(),
  role: z.string(),
  can_assign: z.boolean(),
  can_receive_assignment: z.boolean(),
  view_information_global: z.boolean(),
});

export type SessionSchema = z.infer<typeof sessionSchema>;

export const userSchema = z.object({
  username: z.string(),
  name: z.string(),
  lastname: z.string(),
  status: z.string(),
  role: z.string(),
  created_at: z.string(),
  updated_at: z.string().nullable(),
});

export type UserSchema = z.infer<typeof userSchema>;

export const userUpdateSchema = z.object({
  username: z.string(),
  name: z.string(),
  lastname: z.string(),
  status: z.string(),
  role: z.string(),
});

export type UserUpdateSchema = z.infer<typeof userUpdateSchema>;
