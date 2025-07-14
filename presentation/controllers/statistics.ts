import { StatisticsAssignmentSchema } from "@/schemas/assignment";
import { StatisticsModel } from "@/models/statistics";
import { SessionModel } from "@/models/session";

export class StatisticsController {
  /**
   * Get all user's assignments statistics.
   *
   * @returns A list of statistics.
   */
  static async getStatisticPersonal(): Promise<StatisticsAssignmentSchema | null> {
    const response = await StatisticsModel.getUserStatistics();
    if (response) return response[0];
    else return null;
  }

  static async getStatisticAllUsers(
    usernames: string[]
  ): Promise<StatisticsAssignmentSchema[]> {
    return await StatisticsModel.getAllStatistics(usernames);
  }
}