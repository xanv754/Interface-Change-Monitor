import Cookies from "js-cookie";
import { TokenSchema } from "@/schemas/token";
import { SessionSchema, UserUpdateSchema } from "@/schemas/user";
import { ConfigurationSchema } from "@/schemas/configuration";

class TokenCookie {
  /**
   * Get token from cookie storage.
   * 
   * @returns Token string or null if not found.
   */
  static getToken(): string | null {
    try {
      let token = Cookies.get("token");
      if (token) return token;
      else return null;
    } catch (error) {
      return null;
    }
  }

  /**
   * Set token to cookie storage.
   * 
   * @param token - Token string to set.
   */
  static setToken(token: TokenSchema): void {
    Cookies.set("token", token.access_token, { sameSite: "strict" });
  }

  /**
   * Clear token from cookie storage.
   */
  static clearToken(): void {
    Cookies.remove("token");
  }
}

export class SessionModel {
  private static url: string = process.env.NEXT_PUBLIC_API_URL ?? "";

  /**
   * Authenticates the user and logs them into the application.
   * 
   * @param username - Username to login.
   * @param password - Password to login.
   * 
   * @returns True if the login was successful, otherwise false.
   */
  static async login(username: string, password: string): Promise<boolean> {
    try {
      const formData = new FormData();
      formData.append("username", username);
      formData.append("password", password);
      const response = await fetch(`${this.url}/token`, {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        const token = await response.json();
        TokenCookie.setToken(token);
        return TokenCookie.getToken() ? true : false;
      } else throw new Error(response.status + ": " + response.statusText);
    } catch (error) {
      console.error(error);
      return false;
    }
  }

  /**
   * Get user information from the server.
   * 
   * @returns User information or null if not found.
   */
  static async getInfoSession(): Promise<SessionSchema | null> {
    try {
      const token = TokenCookie.getToken();
      if (token) {
        const response = await fetch(`${this.url}/user/info`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (response.ok) {
          const user = await response.json();
          return user;
        } else throw new Error(response.status + ": " + response.statusText);
      } else return null;
    } catch (error) {
      console.error(error);
      return null;
    }
  }

  /**
   * Get configuration system from the server.
   * 
   * @returns Configuration system, otherwise null.
   */
  static async getConfigurationSystem(): Promise<ConfigurationSchema | null> {
    try {
      const token = TokenCookie.getToken();
      if (token) {
        const response = await fetch(`${this.url}/configuration`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (response.ok) {
          const configuration = await response.json();
          return configuration;
        } else throw new Error(response.status + ": " + response.statusText);
      } else return null;
    } catch (error) {
      console.error(error);
      return null;
    }
  }

  /**
   * Get token session from cookie storage.
   * 
   * @returns Token string or null if not found.
   */
  static getToken(): string | null {
    try {
      return TokenCookie.getToken();
    } catch (error) {
      console.error(error);
      return null;
    }
  }

  /**
   * Update user information.
   * 
   * @param user - User information to update.
   * 
   * @returns True if the update was successful, otherwise false.
   */
  static async updateInfo(user: UserUpdateSchema): Promise<boolean> {
    try {
      const token = TokenCookie.getToken();
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

  /**
   * Update password of a user.
   * 
   * @param newPassword - New password to update.
   * 
   * @returns True if the update was successful, otherwise false.
   */
  static async updatePassword(newPassword: string): Promise<boolean> {
    try {
      const token = TokenCookie.getToken();
      if (token) {
        const response = await fetch(`${this.url}/user/info/password?new_password=${newPassword}`, {
          method: "PATCH",
          headers: {
            Authorization: `Bearer ${token}`,
          }
        });
        if (response.ok) return true;
        else throw new Error(response.status + ": " + response.statusText);
      } else throw new Error("Token user not found");
    } catch (error) {
      console.error(error);
      return false;
    }
  }

  /**
   * Update configuration of the system.  
   * 
   * @param newConfig - New configuration to update.
   * 
   * @returns True if the update was successful, otherwise false.
   */
  static async updateConfiguration(newConfig: ConfigurationSchema): Promise<boolean> {
    try {
      const token = TokenCookie.getToken();
      if (token) {
        const response = await fetch(`${this.url}/configuration/new`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(newConfig),
        });
        if (response.ok) return true;
        else throw new Error(response.status + ": " + response.statusText);
      } else throw new Error("Token user not found");
    } catch (error) {
      console.error(error);
      return false;
    }
  }

  /**
   * Clear token of session from cookie storage.
   */
  static logout(): void {
    try {
      TokenCookie.clearToken();
    } catch (error) {
      console.error(error);
    }
  }
}
