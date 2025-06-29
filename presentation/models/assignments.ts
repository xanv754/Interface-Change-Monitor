import { NewAssignmentSchema, ReassignmentSchema, UpdateAssignmentSchema } from "@/schemas/assignment";
import { SessionModel } from "@/models/session";

export class AssignmentModel {
  private static url: string = process.env.NEXT_PUBLIC_API_URL ?? "";

  /**
   * Assign interfaces with changes to a user.
   *
   * @param assignments - Assignments to insert.
   *
   * @returns True if the assignments were successful, otherwise false.
   */
  static async newAssignments(
    assignments: NewAssignmentSchema[]
  ): Promise<boolean> {
    try {
      const token = SessionModel.getToken();
      if (token) {
        const response = await fetch(`${this.url}/assignments/new`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(assignments),
        });
        if (response.ok) return true;
        else throw new Error(response.status + ": " + response.statusText);
      } else throw new Error("Token not found");
    } catch (error) {
      console.error(error);
      return false;
    }
  }

  /**
   * Reassign interfaces with changes to a user.
   *
   * @param assignments - Assignments to reassign.
   *
   * @returns True if the assignments were successful, otherwise false.
   */
  static async reassignment(
    assignments: ReassignmentSchema[]
  ): Promise<boolean> {
    try {
      const token = SessionModel.getToken();
      if (token) {
        const response = await fetch(`${this.url}/assignments/reassign`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(assignments),
        });
        if (response.ok) return true;
        else throw new Error(response.status + ": " + response.statusText);
      } else throw new Error("Token not found");
    } catch (error) {
      console.error(error);
      return false;
    }
  }

  /**
   * Automatically assigns all modified interfaces to the chosen users.
   * 
   * @param users - Users to assign.
   *
   * @returns True if the assignments were successful, otherwise false.
   */
  static async automaticAssignment(users: string[]): Promise<boolean> {
    try {
      const token = SessionModel.getToken();
      if (token) {
        const response = await fetch(`${this.url}/assignments/automatic`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(users),
        });
        if (response.ok) return true;
        else throw new Error(response.status + ": " + response.statusText);
      } else throw new Error("Token not found");
    } catch (error) {
      console.error(error);
      return false;
    }
  }

  /**
   * Update assignments status.
   *
   * @param assignments - Assignments to update status.
   *
   * @returns True if the assignments were successful, otherwise false.
   */
  static async updateStatusAssignments(
    assignments: UpdateAssignmentSchema[]
  ): Promise<boolean> {
    try {
      const token = SessionModel.getToken();
      if (token) {
        const response = await fetch(`${this.url}/assignments/status`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(assignments),
        });
        if (response.ok) return true;
        else throw new Error(response.status + ": " + response.statusText);
      } else throw new Error("Token not found");
    } catch (error) {
      console.error(error);
      return false;
    }
  }

}
