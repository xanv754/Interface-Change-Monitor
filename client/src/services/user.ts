import { TokenSchema } from "@/schemas/token";
import { UserSchema, UserResponseSchema, UserUpdateDataBodySchema, UserUpdatePasswordBodySchema } from "@/schemas/user";


const url = `${process.env.NEXT_PUBLIC_API_URL}`;

export class UserService {
    static async login(username: string, password: string): Promise<TokenSchema | null> {
        return fetch(`${url}/login`, {
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

    static async getInfoUser(token: string): Promise<UserResponseSchema | null> {
        return fetch(`${url}/operator/info/me`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': `Bearer ${token}`,
            }
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return response.json();
        })
        .then(data => {
            if (!data) return null;
            return data as UserResponseSchema;
        })
        .catch(error => {
            console.error(error);
            return null;
        });
    }

    static async updateInfo(token: string, data: UserUpdateDataBodySchema): Promise<boolean> {
        return fetch(`${url}/operator/info/me`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return true;
        })
        .catch(error => {
            console.error(error);
            return false;
        });
    }

    static async updatePassword(token: string, data: UserUpdatePasswordBodySchema): Promise<boolean> {
        return fetch(`${url}/operator/info/me/password`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(data),
        })
        .then(response => {
            if (!response.ok) throw new Error(response.statusText);
            return true;
        })
        .catch(error => {
            console.error(error);
            return false;
        }); 
    }
}