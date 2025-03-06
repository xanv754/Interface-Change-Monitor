import { TokenSchema } from "@/schemas/token";
import { UserLogginResponseSchema, UserUpdateInfoRequestSchema, UserUpdatePasswordRequestSchema } from "@/schemas/user";

const url = `${process.env.NEXT_PUBLIC_API_URL}`;

/** @class UserService representation of all available API requests to manage the logged-in user. */
export class UserService {
   /**
    * Requests the API to retrieve the token of the logged-in user.
    *
    * @param {string} username The username of the user.
    * @param {string} password The password of the user.
    * @return {TokenSchema} The token of the logged-in user.
    */
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

  /**
    * Requests the API to retrieve the logged-in user's information.
    *
    * @param {string} token The logged-in user's token.
    * @return {UserLogginResponseSchema} The logged-in user's information.
    */
    static async getInfoUser(token: string): Promise<UserLogginResponseSchema | null> {
        return fetch(`${url}/operator/info/me`, {
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
            if (!data) return null;
            return data as UserLogginResponseSchema;
        })
        .catch(error => {
            console.error(error);
            return null;
        });
    }

  /**
    * Requests the API to update the logged-in user's information.
    * 
    * @param {string} token The logged-in user's token.
    * @param {UserUpdateInfoRequestSchema} data The data to update the logged-in user's information.
    * @return {boolean} The status of the completion of the requested operation.
    */
    static async updateInfo(token: string, data: UserUpdateInfoRequestSchema): Promise<boolean> {
        return fetch(`${url}/operator/info/me`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
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

  /**
    * Requests the API to update the logged-in user's password.
    * 
    * @param {string} token The logged-in user's token.
    * @param {UserUpdatePasswordRequestSchema} data The data to update the logged-in user's password.
    * @return {boolean} The status of the completion of the requested operation.
    */
    static async updatePassword(token: string, data: UserUpdatePasswordRequestSchema): Promise<boolean> {
        return fetch(`${url}/operator/info/me/password`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
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