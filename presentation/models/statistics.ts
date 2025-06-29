import { StatisticsAssignmentSchema } from "@/schemas/assignment";
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
  static async getStatisticsAssignments(
    usernames: string[]
  ): Promise<StatisticsAssignmentSchema[]> {
    try {
      const token = SessionModel.getToken();
      if (token) {
        const response = await fetch(`${this.url}/statistics/assignments/user`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ usernames: usernames }),
        });
        if (response.ok) return await response.json();
        else throw new Error(response.status + ": " + response.statusText);
      } else throw new Error("Token not found");
    } catch (error) {
      console.error(error);
      return [];
    }
  }
}