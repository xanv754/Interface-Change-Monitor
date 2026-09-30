import { z } from "zod";
import { StatisticsAssignmentSchema, statisticsAssignmentSchema } from "@/schemas/assignment";
import { SessionModel } from "@/models/session";

export class StatisticsModel {
  private static url: string = process.env.NEXT_PUBLIC_API_URL ?? "";

  /**
   * Get all user assignments statistics.
   *
   * @param usernames - Usernames to get statistics.
   *
   * @returns A list of statistics.
   */
  static async getAllStatistics(
    usernames: string[]
  ): Promise<StatisticsAssignmentSchema[]> {
    try {
      const token = SessionModel.getToken();
      if (token) {
        const response = await fetch(`${this.url}/statistics/assignments/all`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ usernames: usernames }),
        });
        if (response.ok) {
          const data = await response.json();
          const parsed = z.array(statisticsAssignmentSchema).safeParse(data);
          if (!parsed.success) {
            console.error(parsed.error);
            return [];
          }
          return parsed.data;
        } else throw new Error(response.status + ": " + response.statusText);
      } else throw new Error("Token not found");
    } catch (error) {
      console.error(error);
      return [];
    }
  }

  static async getUserStatistics(): Promise<StatisticsAssignmentSchema[]> {
    try {
      const token = SessionModel.getToken();
      if (token) {
        const response = await fetch(`${this.url}/statistics/assignments/user`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });
        if (response.ok) {
          const data = await response.json();
          const parsed = z.array(statisticsAssignmentSchema).safeParse(data);
          if (!parsed.success) {
            console.error(parsed.error);
            return [];
          }
          return parsed.data;
        } else throw new Error(response.status + ": " + response.statusText);
      } else throw new Error("Token not found");
    } catch (error) {
      console.error(error);
      return [];
    }
  }
}