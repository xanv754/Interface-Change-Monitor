import { InterfaceChangeSchema, PaginatedChangesSchema } from "@/schemas/interface";
import { InterfaceModel } from "@/models/interfaces";

export class InterfaceController {
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
    return await InterfaceModel.getInterfaceChanges(page, pageSize);
  }

  /**
   * Get all network interfaces with changes, iterating over every page.
   *
   * @param pageSize - Number of items per request while iterating.
   *
   * @returns Full list of interfaces with changes.
   */
  static async getAllInterfaceChanges(
    pageSize: number = 1000,
  ): Promise<InterfaceChangeSchema[]> {
    const first = await InterfaceModel.getInterfaceChanges(1, pageSize);
    let items = [...first.items];
    for (let page = 2; page <= first.total_pages; page++) {
      const response = await InterfaceModel.getInterfaceChanges(page, pageSize);
      items = items.concat(response.items);
    }
    return items;
  }
}
