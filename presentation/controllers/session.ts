import Cookies from "js-cookie";
import { TokenModel } from "@/models/session";
import { UserLoggedModel } from "@/models/users";

class TokenCookie {
  static getToken(): string | null {
    try {
      let token = Cookies.get("token");
      if (token) return token;
      else return null;
    } catch (error) {
      return null;
    }
  }

  static setToken(token: TokenModel): void {
    Cookies.set("token", token.access_token, { sameSite: "strict" });
  }

  static clearToken(): void {
    Cookies.remove("token");
  }
}

export class SessionController {
  private static url: string = process.env.NEXT_PUBLIC_API_URL ?? "";

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

  static async getUser(): Promise<UserLoggedModel | null> {
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

  static getToken(): string | null {
    try {
      return TokenCookie.getToken();
    } catch (error) {
      console.error(error);
      return null;
    }
  }

  static logout(): void {
    try {
      TokenCookie.clearToken();
    } catch (error) {
      console.error(error);
    }
  }
}
