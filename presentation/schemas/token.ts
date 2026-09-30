import { z } from "zod";

export const tokenSchema = z.object({
  access_token: z.string(),
  token_type: z.string(),
});

export type TokenSchema = z.infer<typeof tokenSchema>;
