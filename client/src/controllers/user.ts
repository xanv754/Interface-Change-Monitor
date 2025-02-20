import { TokenSchema } from "@schemas/token";
import { UserSchema } from "@schemas/user";

const url = process.env.NEXT_PUBLIC_API_URL;

export class UserController {

    static async login(username: string, password: string): Promise<TokenSchema | null> {
        try {
            const response = await fetch(`${url}/login`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                  username: username,
                  password: password,
                }).toString(),
            });
            if (response.ok) {
                let res = await response.json();
                return res;
            }
            else throw new Error(response.statusText);
        } catch (error) {
            console.error(error);
            return null;
        }
    }

    static async myInfo(token: string): Promise<UserSchema | null> {
        try {
            const response = await fetch(`${url}/operator/info/me`, {
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
            else throw new Error(response.statusText);
        } catch (error) {
            console.error(error);
            return null;
        }
    }

    static async changeName(token: string, data: { name: string, lastname: string}): Promise<boolean> {
        try {
            const response = await fetch(`${url}/operator/info/me`, {
                method: 'PUT',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(data),
            });
            if (response.ok) {
                return true;
            }
            else throw new Error(response.statusText);
        } catch (error) {
            console.error(error);
            return false;
        }
    }
}