import { PaginatedChangesSchema } from "@/schemas/interface";
import { SessionModel } from "@/models/session";

export class InterfaceModel {
  private static url: string = process.env.NEXT_PUBLIC_API_URL ?? "";

  /**
   * Get a page of network interfaces with changes made during the current day.
   *
   * @param page - Page number to fetch.
   * @param pageSize - Number of items per page.
   *
   * @returns Paginated interfaces with changes.
   */
  static async getInterfaceChanges(
    page: number = 1,
    pageSize: number = 100,
  ): Promise<PaginatedChangesSchema> {
    const empty: PaginatedChangesSchema = {
      items: [],
      total: 0,
      page,
      page_size: pageSize,
      total_pages: 0,
    };
    try {
      const token = SessionModel.getToken();
      if (token) {
        const response = await fetch(
          `${this.url}/changes?page=${page}&page_size=${pageSize}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );
        if (response.ok) return await response.json();
        else throw new Error(response.status + ": " + response.statusText);
      } else throw new Error("Token not found");
    } catch (error) {
      console.error(error);
      return empty;
    }
  }
}
