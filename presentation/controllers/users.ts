import { UserStatusTypes, RoleTypes } from "@/constants/types";
import { SessionModel } from "@/models/session";
import { UserModel } from "@/models/users";
import { UserSchema, UserUpdateSchema } from "@/schemas/user";

export class UserController {
  /**
   * Get all users.
   *
   * @returns List of users.
   */
  static async getAllUsers(): Promise<UserModel[]> {
    const users = await UserModel.getUsers();
    return users;
  }

  /**
   * Get all active users.
   *
   * @returns List of active users.
   */
  static async getAllActiveUsers(): Promise<UserModel[]> {
    const users = await UserModel.getUsers();
    return users.filter((user) => user.status === UserStatusTypes.ACTIVE);
  }

  /**
   * Get all available users to assign interfaces.
   *
   * @returns List of active users.
   */
  static async getAvailaibleAssignUsers(): Promise<UserModel[]> {
    const config = await SessionModel.getConfigurationSystem();
    if (!config) return [];
    const users = await UserModel.getUsers();
    return users.filter((user: UserSchema) => {
      (config.can_receive_assignment.root && user.role === RoleTypes.ROOT) ||
        (config.can_receive_assignment.admin &&
          user.role === RoleTypes.ADMIN) ||
        (config.can_receive_assignment.user && user.role === RoleTypes.USER);
    });
  }

  /**
   * Inactivate a user.
   *
   * @param user - User to inactivate.
   *
   * @returns True if the inactivation was successful, otherwise false.
   */
  static async inactivateUser(user: UserSchema): Promise<boolean> {
    const updateUser: UserUpdateSchema = {
      username: user.username,
      name: user.name,
      lastname: user.lastname,
      status: UserStatusTypes.INACTIVE,
      role: user.role,
    };
    return await UserModel.updateUser(updateUser);
  }

  /**
   * Inactivate a user.
   *
   * @param user - User to inactivate.
   *
   * @returns True if the delete was successful, otherwise false.
   */
  static async deleteUser(user: UserSchema): Promise<boolean> {
    const updateUser: UserUpdateSchema = {
      username: user.username,
      name: user.name,
      lastname: user.lastname,
      status: UserStatusTypes.DELETED,
      role: user.role,
    };
    return await UserModel.updateUser(updateUser);
  }
}
