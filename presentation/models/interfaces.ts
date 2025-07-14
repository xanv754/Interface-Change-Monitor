import { InterfaceChangeSchema } from "@/schemas/interface";
import { SessionModel } from "@/models/session";

export class InterfaceModel {
  private static url: string = process.env.NEXT_PUBLIC_API_URL ?? "";

  /**
   * Get all network interfaces with changes made during the current day.
   *
   * @returns Interface with changes.
   */
  static async getInterfaceChanges(): Promise<InterfaceChangeSchema[]> {
    try {
      const token = SessionModel.getToken();
      if (token) {
        const response = await fetch(`${this.url}/changes`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
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
