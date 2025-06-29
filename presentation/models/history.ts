import { InterfaceAssignedSchema } from "@/schemas/interface";
import { SessionModel } from "@/models/session";

export class HistoryModel {
  private static url: string = process.env.NEXT_PUBLIC_API_URL ?? "";

  /**
   * Get all assignments by status.
   *
   * @param status - Status to get assignments.
   *
   * @returns A list of interfaces assigned with a status.
   */
  static async getHistoryByStatus(
    status: string
  ): Promise<InterfaceAssignedSchema[]> {
    try {
      const token = SessionModel.getToken();
      if (token) {
        const response = await fetch(`${this.url}/history/assignments`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ status: status }),
        });
        if (response.ok) return await response.json();
        else throw new Error(response.status + ": " + response.statusText);
      } else throw new Error("Token not found");
    } catch (error) {
      console.error(error);
      return [];
    }
  }

  /**
   * Get all assignments completed in a month.
   *
   * @param month - Month to get assignments. Default is current month.
   *
   * @returns A list of interfaces assigned in a month.
   */
  static async getHistoryMonth(
    month: string
  ): Promise<InterfaceAssignedSchema[]> {
    try {
      const token = SessionModel.getToken();
      if (token) {
        const response = await fetch(
          `${this.url}/history/user?month=${month}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        if (response.ok) return await response.json();
        else throw new Error(response.status + ": " + response.statusText);
      } else throw new Error("Token not found");
    } catch (error) {
      console.error(error);
      return [];
    }
  }

  /**
   * Get all assignments completed in a month of all users.
   *
   * @param month - Month to get assignments. Default is current month.
   * @param usernames - Usernames to get assignments.
   *
   * @returns A list of interfaces assigned in a month.
   */
  static async getAllHistoryUsers(
    month: string,
    usernames: string[]
  ): Promise<InterfaceAssignedSchema[]> {
    try {
      const token = SessionModel.getToken();
      if (token) {
        const response = await fetch(`${this.url}/history/all`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            month: month,
            usernames: usernames,
          }),
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
