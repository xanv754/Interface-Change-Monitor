import Cookies from "js-cookie";

export class Token {
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
