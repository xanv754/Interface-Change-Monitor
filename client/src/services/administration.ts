import { UserResponseSchema, UserUpdateProfileRequestSchema, UserUpdateAccountRequestSchema } from "@/schemas/user";
import { ChangeResponseSchema } from "@/schemas/changes";

const url = `${process.env.NEXT_PUBLIC_API_URL}/administration`;

/** @class AdministrationService representation of all available API requests to manage interface change monitoring and user profiles. */
export class AdministrationService {
   /**
    * Requests the API to retrieve all interface data with changes.
    *
    * @param {token} string The logged-in user's token.
    * @return {ChangeResponseSchema[]} An array of interface data with changes.
    */
    static async getChanges(token: string): Promise<ChangeResponseSchema[]> {
        return fetch(`${url}/changes`, {
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

   /**
    * Requests the API to retrieve all users.
    *
    * @param {token} string The logged-in user's token.
    * @return {UserResponseSchema[]} An array of all users.
    */
    static async getAllUsers(token: string): Promise<UserResponseSchema[]> {
        return fetch(`${url}/operator/info/all`, {
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
            return data as UserResponseSchema[];
        })
        .catch(error => {
            console.error(error);
            return [];
        });
    }

  /**
    * Requests the API to update the user's profile.
    *
    * @param {token} string The logged-in user's token.
    * @param {data} UserUpdateProfileRequestSchema The data to update the user's profile.
    * @return {boolean} The status of the completion of the requested operation.
    */
    static async updateProfileUser(token: string, data: UserUpdateProfileRequestSchema): Promise<boolean> {
        return fetch(`${url}/operator/info/profile`, {
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
    * Requests the API to update the user's account.
    *
    * @param {token} string The logged-in user's token.
    * @param {data} UserUpdateAccountRequestSchema The data to update the user's account.
    * @return {boolean} The status of the completion of the requested operation.
    */
    static async updateAccountUser(token: string, data: UserUpdateAccountRequestSchema): Promise<boolean> {
        return fetch(`${url}/operator/info/account`, {
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
    * Requests the API to delete an user.
    *
    * @param {token} string The logged-in user's token.
    * @param {username} string The username of the user to delete.
    * @return {boolean} The status of the completion of the requested operation.
    */    
    static async deleteUser(token: string, username: string): Promise<boolean> {
        return fetch(`${url}/operator?username=${username}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
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