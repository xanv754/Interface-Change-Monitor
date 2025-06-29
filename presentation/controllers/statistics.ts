import { StatisticsAssignmentSchema } from "@/schemas/assignment";
import { StatisticsModel } from "@/models/statistics";
import { SessionModel } from "@/models/session";

export class StatisticsController {
  /**
   * Get all user's assignments statistics.
   *
   * @param usernames - Usernames to get statistics.
   *
   * @returns A list of statistics.
   */
  static async getStatisticsAssignments(): Promise<StatisticsAssignmentSchema | null> {
    const user = await SessionModel.getInfoSession();
    if (!user) return null;
    const statistics = await StatisticsModel.getStatisticsAssignments([user.username]);
    if (statistics.length > 0) return statistics[0];
    return null;
  }

  static async getStatisticsAssignmentsUsers(
    usernames: string[]
  ): Promise<StatisticsAssignmentSchema[]> {
    return await StatisticsModel.getStatisticsAssignments(usernames);
  }
}