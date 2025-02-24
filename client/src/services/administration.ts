import { UserSchema, UserProfileBodySchema, UserAccountBodySchema } from "@/schemas/user";
import { ChangeResponseSchema } from "@/schemas/changes";

const url = `${process.env.NEXT_PUBLIC_API_URL}/administration`;

export class AdministrationService {
    static async getChanges(token: string): Promise<ChangeResponseSchema[]> {
        return fetch(`${url}/changes`, {
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
            return data as ChangeResponseSchema[];
        })
        .catch(error => {
            console.error(error);
            return [];
        });
    }

    static async getAllUsers(token: string): Promise<UserSchema[]> {
        return fetch(`${url}/operator/info/all`, {
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
            return data as UserSchema[];
        })
        .catch(error => {
            console.error(error);
            return [];
        });
    }

    static async updateProfileUser(token: string, data: UserProfileBodySchema): Promise<boolean> {
        return fetch(`${url}/operator/info/profile`, {
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

    static async updateAccountUser(token: string, data: UserAccountBodySchema): Promise<boolean> {
        return fetch(`${url}/operator/info/account`, {
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

    static async deleteUser(token: string, username: string): Promise<boolean> {
        return fetch(`${url}/operator?username=${username}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': `Bearer ${token}`,
            }
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