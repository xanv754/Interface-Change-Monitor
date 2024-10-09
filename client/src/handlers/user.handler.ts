import type { AssignmentStatusModel } from "../models/assignStatus";
import type { UserModel } from "../models/user";
import { ErrorRequest } from '../class/Error';

class HandlerRequestUser {
  private url: string = import.meta.env.PUBLIC_API;

  async getUsers(token: string): Promise<UserModel[] | ErrorRequest> {
    try {
      let options = {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
      }
      const response = await fetch(`${this.url}/api/v1/users`, options);
      if (!response.ok) throw new ErrorRequest(`${response.status}`);
      const users: UserModel[] = await response.json();
      return users;
    } catch (error) {
      return error;
    }
  }

  async getDataUser(token: string, username: string): Promise<UserModel | ErrorRequest> {
    try {
      let options = {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
      }
      const response = await fetch(`${this.url}/api/v1/users/username=${username}`, options);
      if (!response.ok) throw new ErrorRequest(`${response.status}`);
      const user: UserModel = await response.json();
      return user;
    } catch (error) {
      return error;
    }
  }

  async updateAssignment(token: string, data: AssignmentStatusModel): Promise<{"message": string} | ErrorRequest> {
    try {
      let options = {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      }
      const response = await fetch(`${this.url}/api/v1/users/reviewed`, options);
      if (!response.ok) throw new ErrorRequest(`${response.status}`);
      const message = await response.json();
      return message;
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
}

export const UserRequest = new HandlerRequestUser();