import type { AdminModel } from "../models/admin";
import { ErrorRequest } from '../class/Error';
import type { UserModel } from "../models/user";

class HandlerRequestAdmin {
    private url: string = import.meta.env.PUBLIC_API;

    async getDataAdmin(token: string, username: string): Promise<AdminModel | ErrorRequest> {
        try {
            let options = {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
            }
            const response = await fetch(`${this.url}/api/v1/users/admin/username=${username}`, options);
            if (!response.ok) throw new ErrorRequest(`${response.status}`);
            const user: AdminModel = await response.json();
            return user;
        } catch (error) {
            return error;
        }
    }

    async getAdmins(token: string): Promise<AdminModel[] | ErrorRequest> {
        try {
            let options = {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
            }
            const response = await fetch(`${this.url}/api/v1/users/admin`, options);
            if (!response.ok) throw new ErrorRequest(`${response.status}`);
            const admins: AdminModel[] = await response.json();
            return admins;
        } catch (error) {
            return error;
        }
    }

    async getAllUsers(token: string): Promise<Array<AdminModel | UserModel>> {
        try {
            let options = {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
            }
            const response = await fetch(`${this.url}/api/v1/users/all`, options);
            if (!response.ok) throw new ErrorRequest(`${response.status}`);
            const users = await response.json();
            return users;
        } catch (error) {
            return error;
        }
    }

    async getUsersPending(token: string): Promise<any[] | ErrorRequest> {
        try {
            let options = {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
            }
            const response = await fetch(`${this.url}/api/v1/users/pending`, options);
            if (!response.ok) throw new ErrorRequest(`${response.status}`);
            const admins: AdminModel[] = await response.json();
            return admins;
        } catch (error) {
            return error;
        }
    }

    async updateUserStatus(token: string, username: string, status:string): Promise<{"message": string} | ErrorRequest> {
        try {
            let options = {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
            }
            const response = await fetch(`${this.url}/api/v1/users/username=${username}/status=${status}`, options);
            if (!response.ok) throw new ErrorRequest(`${response.status}`);
            const res = await response.json();
            return res;
        } catch (error) {
            return error;
        }        
    }

    async autoAssignment(token: string, usernames: string[]): Promise<{"message": string} | ErrorRequest> {
        try {
            let options = {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "usernames": usernames
                }),
            }
            const response = await fetch(`${this.url}/api/v1/users/autoAssignment`, options);
            if (!response.ok) throw new ErrorRequest(`${response.status}`);
            const res = await response.json();
            return res;
        } catch (error) {
            return error;
        }         
    }

    async addAssignElement(token: string, username: string, idElement: string): Promise<{"message": string} | ErrorRequest>{
        try {
            let options = {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
            }
            const response = await fetch(`${this.url}/api/v1/users/assigned=${username}/element=${idElement}`, options);
            if (!response.ok) throw new ErrorRequest(`${response.status}`);
            const res = await response.json();
            return res;
        } catch (error) {
            return error;
        }      
    }

    async updateName(token: string, username: string, new_name: string): Promise<{"message": string} | ErrorRequest> {
        try {
            let options = {
              method: 'PUT',
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
              }
            }
            const response = await fetch(`${this.url}/api/v1/users/username=${username}/name=${new_name}`, options);
            if (!response.ok) throw new ErrorRequest(`${response.status}`);
            const message = await response.json();
            return message;
        } catch (error) {
            return error;
        }
    }

    async updateLastname(token: string, username: string, new_lastname: string): Promise<{"message": string} | ErrorRequest> {
        try {
            let options = {
              method: 'PUT',
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
              }
            }
            const response = await fetch(`${this.url}/api/v1/users/username=${username}/lastname=${new_lastname}`, options);
            if (!response.ok) throw new ErrorRequest(`${response.status}`);
            const message = await response.json();
            return message;
        } catch (error) {
            return error;
        }
    }

    async updatePassword(token: string, username: string, new_password: string): Promise<{"message": string} | ErrorRequest> {
        try {
            let options = {
              method: 'PUT',
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
              }
            }
            const response = await fetch(`${this.url}/api/v1/users/username=${username}/password=${new_password}`, options);
            if (!response.ok) throw new ErrorRequest(`${response.status}`);
            const message = await response.json();
            return message;
        } catch (error) {
            return error;
        }
    }

    async deleteUser(token: string, username: string): Promise<{"message": string} | ErrorRequest> {
        try {
            let options = {
              method: 'DELETE',
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
              }
            }
            const response = await fetch(`${this.url}/api/v1/users/username=${username}`, options);
            if (!response.ok) throw new ErrorRequest(`${response.status}`);
            const message = await response.json();
            return message;
        } catch (error) {
            return error;
        }
    }

    async permissionChangePassword(token: string, username: string, permissionStatus: string): Promise<boolean | ErrorRequest> {
        try {
            let options = {
              method: 'PUT',
              headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
              }
            }
            const response = await fetch(`${this.url}/api/v1/users/username=${username}/permission=${permissionStatus}`, options);
            if (!response.ok) throw new ErrorRequest(`${response.status}`);
            return true;
        } catch (error) {
            return error;
        }
    }
}

export const AdminRequest = new HandlerRequestAdmin();