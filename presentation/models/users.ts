import { SessionModel } from "@/models/session";
import { UserSchema, UserUpdateSchema } from "@/schemas/user";

export class UserModel {
  private static url: string = process.env.NEXT_PUBLIC_API_URL ?? "";

  static async getUsers(): Promise<UserSchema[]> {
    try {
      const token = SessionModel.getToken();
      if (token) {
        const response = await fetch(`${this.url}/user/all`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (response.ok) return await response.json();
        else throw new Error(response.status + ": " + response.statusText);
      } else throw new Error("Token user not found");
    } catch (error) {
      console.error(error);
      return [];
    }
  }

  /**
   * Update user information.
   *
   * @param user - User information to update.
   *
   * @returns True if the update was successful, otherwise false.
   */
  static async updateUser(user: UserUpdateSchema): Promise<boolean> {
    try {
      const token = SessionModel.getToken();
      if (token) {
        const response = await fetch(`${this.url}/user/info`, {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(user),
        });
        if (response.ok) return true;
        else throw new Error(response.status + ": " + response.statusText);
      } else throw new Error("Token user not found");
    } catch (error) {
      console.error(error);
      return false;
    }
  }
}
