import { RequestLogin } from "../handlers/login.handler";
import type { RegisterModel } from "../models/register";
import { userType } from "../../constants/userType";
import type { AccessModel } from "../models/access";
import type { AdminModel } from "../models/admin";
import type { LoginModel } from "../models/login";
import type { UserModel } from "../models/user";
import { ErrorRequest } from "../class/Error";


class ControllerLogin {

    async register(userData: RegisterModel): Promise<Number> {
        try {
            const response = await RequestLogin.register(userData);
            if (response instanceof ErrorRequest) throw response;
            else return 1
        } catch (error) {
            console.error(error);
            if (error.status == "409") return 2
            return 0;
        }
    }

    async login(userData: LoginModel): Promise<AccessModel> {
        try {
            const response = await RequestLogin.login(userData);
            if (response instanceof ErrorRequest) throw response;
            return response;
        } catch(error) {
            console.error(error);
            return null;
        }
    }

    async isActiveUser(token: string, userType: string): Promise<boolean> {
        try {
            const response = await RequestLogin.getDataUser(token);
            if (response instanceof ErrorRequest) throw response;
            if ((response.type) && (response.type == userType)) return true;
            else return false;
        } catch (error) {
            console.error(error);
            return false;
        }
    }

    async getDataUser(token: string): Promise<UserModel | AdminModel > {
        try {
            const response = await RequestLogin.getDataUser(token);
            if (response instanceof ErrorRequest) throw response;
            return response;
        } catch(error) {
            console.error(error);
            return null;
        }
    }

    async getUser(token: string): Promise<UserModel> {
        try {
            const response = await RequestLogin.getUser(token);
            if (response instanceof ErrorRequest) throw response;
            if (response.type == userType.user) return response;
            else return null;
        } catch(error) {
            console.error(error);
            return null;
        }
    }

    async forgotPassword(username: string, newPassword: string): Promise<boolean> {
        try {
            const response = await RequestLogin.forgotPassword(username, newPassword);
            if (response instanceof ErrorRequest) throw response;
            return true;
        } catch(error) {
            console.error(error);
            return false;
        }
    }

}

export const LoginController = new ControllerLogin();