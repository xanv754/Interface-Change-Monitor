import { AssignmentStatusTypes } from "@/constants/types";
import { HistoryModel } from "@/models/history";
import { InterfaceAssignedSchema } from "@/schemas/interface";
import { DateHandler } from "@/utils/date";

export class HistoryController {
  /**
   * Get all assignments pending.
   *
   * @returns A list of interfaces assigned with pending status.
   */
  static async getHistoryPending(): Promise<InterfaceAssignedSchema[]> {
    return await HistoryModel.getHistoryByStatus(AssignmentStatusTypes.PENDING);
  }

  /**
   * Get all assignments reviewed.
   *
   * @returns A list of interfaces assigned with reviewed status.
   */
  static async getHistoryReviewed(): Promise<InterfaceAssignedSchema[]> {
    const inspected_assignments = await HistoryModel.getHistoryByStatus(
      AssignmentStatusTypes.INSPECTED
    );
    const rediscovered_assignments = await HistoryModel.getHistoryByStatus(
      AssignmentStatusTypes.REDISCOVERED
    );
    return [...inspected_assignments, ...rediscovered_assignments];
  }

  /**
   * Get all assignments reviewed in a month.
   *
   * @param date - Month to get assignments. Default is current month.
   *
   * @returns A list of interfaces assigned in a month.
   */
  static async getHistoryReviewedMonth(
    date: string = DateHandler.getYearMonth()
  ): Promise<InterfaceAssignedSchema[]> {
    return await HistoryModel.getHistoryMonth(date);
  }

  /**
   * Get all assignments completed in a month of all users.
   *
   * @param date - Month to get assignments. Default is current month.
   * @param usernames - Usernames to get assignments.
   *
   * @returns A list of interfaces assigned in a month.
   */
  static async getAllHistoryUsers(
    usernames: string[],
    date: string = DateHandler.getYearMonth()
  ): Promise<InterfaceAssignedSchema[]> {
    return await HistoryModel.getAllHistoryUsers(date, usernames);
  }

  static async getDateAvailableToConsultHistory(): Promise<string[]> {
    return await HistoryModel.getDateAvailableToConsultHistory();
  }
}
