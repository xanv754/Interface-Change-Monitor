import { InterfaceChangeSchema } from "@/schemas/interface";
import { InterfaceModel } from "@/models/interfaces";

export class InterfaceController {
  /**
   * Get all network interfaces with changes made during the current day.
   *
   * @returns Interface with changes.
   */
  static async getInterfaceChanges(): Promise<InterfaceChangeSchema[]> {
    return await InterfaceModel.getInterfaceChanges();
  }
}
