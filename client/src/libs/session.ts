import { UserShortInfoResponseSchema } from "@schemas/user";
import { ConfigurationResponseSchema } from "@schemas/configuration";
import { TokenSchema } from '@schemas/token';
import { UserService } from "../services/user";
import Cookies from "js-cookie";

/** @class Token representation of the token of the logged-in user saved in the browser's cookies. */
class Token {
   /**
    * Returns the token of the logged-in user saved in the browser's cookies.
    * 
    * @return {string | null} The token of the logged-in user.
    */
    static getToken(): string | null {
        return Cookies.get('token');
    }
    
   /**
    * Saves the token of the logged-in user in the browser's cookies.
    * 
    * @param {token} string The token of the logged-in user.
    */
    static setToken(token: string): void {
        Cookies.set('token', token, {
            sameSite: 'strict'
        });
    }

   /**
    * Deletes the token of the logged-in user from the browser's cookies.
    */
    static clearToken(): void {
        Cookies.remove('token');
    }
}

/** @class CurrentSession representation of the current session of the logged-in user. */
export class CurrentSession {
   /**
    * Saves the token of the logged-in user in the browser's cookies and the information of the logged-in user.
    * 
    * @param {token} TokenSchema The token of the logged-in user.
    * @return {UserShortInfoResponseSchema | null} The information of the logged-in user.
    */
    static async saveInfo(token: TokenSchema): Promise<UserShortInfoResponseSchema | null> {
        try {
            if (token.access_token) {
                Token.setToken(token.access_token);
                const user = await UserService.getInfoUser(token.access_token);
                if (user) {
                    const dataUser: UserShortInfoResponseSchema = {
                        username: user.username,
                        name: user.name,
                        lastname: user.lastname,
                        profile: user.profile,
                    }
                    const dataConfig = user.configuration;
                    sessionStorage.setItem('user', JSON.stringify(dataUser));
                    sessionStorage.setItem('config', JSON.stringify(dataConfig));
                    return dataUser;
                }
            }
            return null;
        } catch (error) {
            console.error(error);
            return null;
        }
    }

    static async saveConfig(config: ConfigurationResponseSchema): Promise<ConfigurationResponseSchema | null> {
        try {
            sessionStorage.removeItem('config');
            sessionStorage.setItem('config', JSON.stringify(config));
            return config;
        } catch (error) {
            console.error(error);
            return null;
        }
    }

   /** 
    * Returns the information of the logged-in user.
    * 
    * @return {UserShortInfoResponseSchema | null} The information of the logged-in user.
    */
    static getInfoUser(): UserShortInfoResponseSchema | null {
        if (CurrentSession.getToken() && sessionStorage.getItem('user')) {
            const user = JSON.parse(sessionStorage.getItem('user') as string) as UserShortInfoResponseSchema;
            if (user) return user;
        }
        return null;
    }

   /** 
    * Returns the information of the configuration of the system.
    * 
    * @return {ConfigurationResponseSchema | null} The information of the configuration of the system.
    */
    static getInfoConfig(): ConfigurationResponseSchema | null {
        if (CurrentSession.getToken() && sessionStorage.getItem('config')) {
            const config = JSON.parse(sessionStorage.getItem('config') as string) as ConfigurationResponseSchema;
            if (config) return config;
        }
        return null;
    }

   /**
    * Returns the token of the logged-in user.
    * 
    * @return {string | null} The token of the logged-in user.
    */
    static getToken(): string | null {
        return Token.getToken();
    }

   /**
    * Deletes the token of the logged-in user and the information of the logged-in user from the browser's cookies.
    */
    static deleteSession() {
        sessionStorage.clear();
        Token.clearToken();
    }
}

