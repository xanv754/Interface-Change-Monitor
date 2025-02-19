import { TokenSchema } from "@/schemas/token";
import { UserSchema } from "@/schemas/user";

export class User {
    private url?: string = process.env.NEXT_PUBLIC_API_URL;
    private username!: string;
    private password!: string;

    constructor(username: string, password: string) {
        this.username = username;
        this.password = password;
    }

    async login(): Promise<TokenSchema | null> {
        const response = await fetch(`${this.url}/login`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
              username: this.username,
              password: this.password,
            }).toString(),
        });
        if (response.ok) {
            let res = await response.json();
            return res;
        }
        return null;
    }

    async myInfo(token: string): Promise<UserSchema | null> {
        const response = await fetch(`${this.url}/operator/info/me`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'Authorization': `Bearer ${token}`,
            },
        });
        if (response.ok) {
            let res = await response.json();
            return res;
        }
        return null;
    }
}