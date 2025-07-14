import { AssignmentStatusTypes } from "@/constants/types";
import { AssignmentModel } from "@/models/assignments";
import { SessionModel } from "@/models/session";
import { NewAssignmentSchema, ReassignmentSchema, UpdateAssignmentSchema } from "@/schemas/assignment";
import { InterfaceChangeSchema } from "@/schemas/interface";

export class AssignmentController {
  /**
   * Assign interfaces with changes to a user.
   *
   * @param interfaces - Interfaces to assign.
   * @param assignUser - User to assign.
   *
   * @returns True if the assignments were successful, otherwise false.
   */
  static async newAssignments(interfaces: InterfaceChangeSchema[], assignUser: string): Promise<boolean> {
    const currentUserSession = await SessionModel.getInfoSession();
    if (!currentUserSession) return false;
    const assignments: NewAssignmentSchema[] = interfaces.map((interfaceChange: InterfaceChangeSchema) => {
      return {
        old_interface_id: Number(interfaceChange.id_old),
        current_interface_id: Number(interfaceChange.id_new),
        username: assignUser,
        assign_by: currentUserSession.username,
        type_status: AssignmentStatusTypes.PENDING
      };
    });
    return await AssignmentModel.newAssignments(assignments);
  }

  /**
   * Reassign interfaces with changes to a user.
   *
   * @param interfaces - Interfaces to reassign.
   * @param assignUser - User to reassign.
   *
   * @returns True if the assignments were successful, otherwise false.
   */
  static async reassignment(interfaces: InterfaceChangeSchema[], assignUser: string): Promise<boolean> {
    const currentUserSession = await SessionModel.getInfoSession();
    if (!currentUserSession) return false;
    const assignments: ReassignmentSchema[] = interfaces.map((interfaceChange: InterfaceChangeSchema) => {
      return {
        old_interface_id: Number(interfaceChange.id_old),
        current_interface_id: Number(interfaceChange.id_new),
        old_username: interfaceChange.username!,
        new_username: assignUser,
        assign_by: currentUserSession.username,
      };
    });
    return await AssignmentModel.reassignment(assignments);
  }

  /**
   * Automatically assigns all modified interfaces to the chosen users.
   *
   * @param users - Users to assign.
   *
   * @returns True if the assignments were successful, otherwise false.
   */
  static async automaticAssignment(users: string[]): Promise<boolean> {
    return await AssignmentModel.automaticAssignment(users);
  }

  /**
   * Update assignments status.
   *
   * @param interfaces - Interfaces to update status.
   * @param status - Status to update.
   *
   * @returns True if the assignments were successful, otherwise false.
   */
  static async updateStatusAssignments(interfaces: InterfaceChangeSchema[], status: string): Promise<boolean> {
    const assignments: UpdateAssignmentSchema[] = interfaces.map((interfaceChange: InterfaceChangeSchema) => {
      return {
        old_interface_id: interfaceChange.id_old,
        current_interface_id: interfaceChange.id_new,
        type_status: status
      };
    });
    return await AssignmentModel.updateStatusAssignments(assignments);
  }
}