import type { RegisterModel } from '../models/register';
import type { AccessModel } from '../models/access';
import type { LoginModel } from '../models/login';
import { ErrorRequest } from '../class/Error';
import type { UserModel } from '../models/user';
import type { AdminModel } from '../models/admin';

class HandlerRequestLogin {
  private url: string = import.meta.env.PUBLIC_API;

  async register(userData: RegisterModel): Promise<{"created": string} | ErrorRequest> {
    try {
      let options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      }
      const response = await fetch(`${this.url}/api/v1/register`, options);
      if (!response.ok) throw new ErrorRequest(`${response.status}`);
      return response.json();
    } catch (error) {
      return error;
    }
  } 

  async login(userData: LoginModel): Promise<AccessModel | ErrorRequest> {
    try {
      let formData = new FormData();
      formData.append("username", userData.user)
      formData.append("password", userData.password)
      let options = {
        method: 'POST',
        body: formData
      }
      const response = await fetch(`${this.url}/api/v1/login`, options);
      if (!response.ok) throw new ErrorRequest(`${response.status}`);
      const access: AccessModel = await response.json();
      return access;
    } catch (error) {
      return error;
    }
  }

  async getDataUser(token: string): Promise<UserModel | AdminModel | ErrorRequest> {
    try {
      let options = {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
      }
      const response = await fetch(`${this.url}/api/v1/myuser`, options);
      if (!response.ok) {
        throw new ErrorRequest(`${response.status}`);
      }
      let res = await response.json();
      return res;
    } catch (error) {
      return error;
    }
  }

  async getUser(token: string): Promise<UserModel | ErrorRequest> {
    try {
      let options = {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
      }
      const response = await fetch(`${this.url}/api/v1/myuser`, options);
      if (!response.ok) {
        throw new ErrorRequest(`${response.status}`);
      }
      let res = await response.json();
      return res;
    } catch (error) {
      return error;
    }
  }

  async forgotPassword(username: string, newPassword: string): Promise<boolean | ErrorRequest> {
    try {
      let options = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
      }
      const response = await fetch(`${this.url}/api/v1/login/username=${username}/newPassword=${newPassword}`, options);
      if (!response.ok) {
        throw new ErrorRequest(`${response.status}`);
      }
      return true;
    } catch (error) {
      return error;
    }
  }
    
}

export const RequestLogin = new HandlerRequestLogin();