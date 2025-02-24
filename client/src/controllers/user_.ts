import { TokenSchema } from "@schemas/token";
import { UserSchema } from "@schemas/user";
import { ChangeResponseSchema } from "@schemas/changes";

const url_base = `${process.env.NEXT_PUBLIC_API_URL}`;
const url_operator = `${process.env.NEXT_PUBLIC_API_URL}/operator/info`;

export class UserController {

    static async login(username: string, password: string): Promise<TokenSchema | null> {
        return fetch(`${url_base}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                username: username,
                password: password,
            }).toString(),
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 401) {
                    console.warn('Invalid username or password');
                    return null;
                } else throw new Error(response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (!data) return null;
            return data as TokenSchema;
        })
        .catch(error => {
            console.error(error);
            return null;
        });
    }

    static async myInfo(token: string): Promise<UserSchema | null> {
        try {
            const response = await fetch(`${url_operator}/me`, {
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
            const response = await fetch(`${url_operator}/me`, {
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

    static async changePassword(token: string, password: string): Promise<boolean> {
        try {
            const response = await fetch(`${url_operator}/me/password`, {
                method: 'PUT',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(password),
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

    static async getAllAssigments(token: string): Promise<ChangeResponseSchema[]> {
        return fetch(`${url_operator}/assignments/all`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            }
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return response.json();
        })
        .then(data => {
            return data as ChangeResponseSchema[];
        })
        .catch(error => {
            console.error(error);
            return [];
        });
    }

    static async getPendingAssigments(token: string): Promise<ChangeResponseSchema[]> {
        return fetch(`${url_operator}/assignments/pending`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            }
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return response.json();
        })
        .then(data => {
            return data as ChangeResponseSchema[];
        })
        .catch(error => {
            console.error(error);
            return [];
        });
    }

    static async updateStatusAssignment(token: string, data: { idAssignment: number, newStatus: string }): Promise<boolean> {
        try {
            const response = await fetch(`${url_operator}/me/assignments/status`, {
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