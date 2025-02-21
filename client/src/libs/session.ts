'use client';

import { UserInfoSchema } from "@/schemas/user";
import { TokenSchema } from '@/schemas/token';
import { UserService } from "@/services/user";
import Cookies from "js-cookie";

class Token {
    static getToken(): string | null {
        return Cookies.get('token');
    }
    
    static setToken(token: string): void {
        Cookies.set('token', token, {
            expires: 1,
            sameSite: 'strict'
        });
    }
    static clearToken(): void {
        Cookies.remove('token');
    }
}

export class CurrentSession {
    static async saveInfo(token: TokenSchema): Promise<boolean> {
        try {
            if (token.access_token) {
                Token.setToken(token.access_token);
                const user = await UserService.getInfoUser(token.access_token);
                console.log(user);
                if (user) {
                    const dataUser: UserInfoSchema = {
                        username: user.username,
                        name: user.name,
                        lastname: user.lastname,
                        profile: user.profile,
                    }
                    const dataConfig = user.configuration;
                    sessionStorage.setItem('user', JSON.stringify(dataUser));
                    sessionStorage.setItem('config', JSON.stringify(dataConfig));
                    return true;
                }
            }
            return false;
        } catch (error) {
            console.error(error);
            return false;
        }
    }

    static getInfo(): UserInfoSchema | null {
        if (sessionStorage.getItem('user')) {
            const user = JSON.parse(sessionStorage.getItem('user') as string) as UserInfoSchema;
            if (user) return user;
        }
        return null;
    }

    static getToken(): string | null {
        return Token.getToken();
    }

    static deleteSession() {
        sessionStorage.clear();
        Token.clearToken();
    }
}

