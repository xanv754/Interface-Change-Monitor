import { SessionModel } from "@/models/session";
import { SessionSchema, UserUpdateSchema } from "@/schemas/user";
import { ConfigurationSchema } from "@/schemas/configuration";

export class SessionController {
  /**
   * Starts a user session (logs in).  
   * 
   * @param username - Username to login.
   * @param password - Password to login.
   * 
   * @returns User logged into the system, otherwise null.
   */
  static async login(username: string, password: string): Promise<SessionSchema | null> {
    const status = await SessionModel.login(username, password);
    if (status) return await SessionModel.getInfoSession();
    else return null;
  }

  /**
   * Get user session.
   * 
   * @returns User logged into the system, otherwise null.
   */
  static async getInfo(): Promise<SessionSchema | null> {
    return await SessionModel.getInfoSession();
  }

  /**
   * Get configuration system.
   * 
   * @returns Configuration system, otherwise null.
   */
  static async getConfigurationSystem(): Promise<ConfigurationSchema | null> {
    return await SessionModel.getConfigurationSystem();
  }

  /**
   * Update user information.
   * 
   * @param user - User information to update.
   * 
   * @returns True if the update was successful, otherwise false.
   */
  static async updateInfo(user: UserUpdateSchema): Promise<boolean> {
    return await SessionModel.updateInfo(user);
  }

  /**
   * Update password of a user.
   * 
   * @param newPassword - New password to update.
   * 
   * @returns True if the update was successful, otherwise false.
   */
  static async updatePassword(newPassword: string): Promise<boolean> {
    return await SessionModel.updatePassword(newPassword);
  }

  static async updateConfiguration(newConfig: ConfigurationSchema): Promise<boolean> {
    return await SessionModel.updateConfiguration(newConfig);
  }

  /**
   * Logout user session.
   */
  static logout(): void {
    SessionModel.logout();
  }
}