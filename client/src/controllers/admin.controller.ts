import { getCurrentMonth, getCurrentDate } from "../../utils/date";
import { assignmentStatus } from "../../constants/assigmentStatus";
import type { InterfaceModel } from "../models/interface";
import { AdminRequest } from "../handlers/admin.handler";
import { UserRequest } from "../handlers/user.handler";
import type { AdminModel } from "../models/admin";
import type { UserModel } from "../models/user";
import { ErrorRequest } from "../class/Error";
import { months } from "../../utils/date";
import { activeUser } from "../../constants/activeUser";

class ControllerAdmin {
    async getData(token: string, username: string): Promise<AdminModel> {
        try {
            const response = await AdminRequest.getDataAdmin(token, username);
            if (response instanceof ErrorRequest) throw response;
            return response;
        } catch(error) {
            console.error(error);
            return null;
        }
    }

    async getUsers(token: string): Promise<UserModel[]> {
        try {
            const response = await UserRequest.getUsers(token);
            if (response instanceof ErrorRequest) throw response;
            return response;
        } catch(error) {
            console.error(error);
            return null;
        }
    }

    async getAllUsers(token: string): Promise<Array<AdminModel | UserModel>> {
        try {
            const response = await AdminRequest.getAllUsers(token);
            if (response instanceof ErrorRequest) throw response;
            return response;
        } catch(error) {
            console.error(error);
            return null;
        }
    }

    async getUsersAdmin(token: string): Promise<AdminModel[]> {
        try {
            const response = await AdminRequest.getAdmins(token);
            if (response instanceof ErrorRequest) throw response;
            return response;
        } catch(error) {
            console.error(error);
            return null;
        }
    }

    async getUsersPending(token: string): Promise<any[]> {
        try {
            const response = await AdminRequest.getUsersPending(token);
            if (response instanceof ErrorRequest) throw response;
            return response;
        } catch(error) {
            console.log(error);
            return null;
        }
    }

    async allowUser(token: string, username: string): Promise<boolean> {
        try {
            const response = await AdminRequest.updateUserStatus(token, username, activeUser.enabled);
            if (response instanceof ErrorRequest) throw response;
            return true;
        } catch(error) {
            console.error(error);
            return false;
        }
    }

    async denyUser(token: string, username: string): Promise<boolean> {
        try {
            const response = await AdminRequest.updateUserStatus(token, username, activeUser.disabled);
            if (response instanceof ErrorRequest) throw response;
            return true;
        } catch(error) {
            console.error(error);
            return false;
        }
    }

    async deleteUser(token: string, username: string): Promise<boolean> {
        try {
            const response = await AdminRequest.deleteUser(token, username);
            if (response instanceof ErrorRequest) throw response;
            return true;
        } catch(error) {
            console.error(error);
            return false;
        }
    }
    
    async autoAssignment(token: string, usernames: string[]): Promise<boolean> {
        try {
            const response = await AdminRequest.autoAssignment(token, usernames);
            if (response instanceof ErrorRequest) throw response;
            return true;
        } catch(error) {
            console.error(error);
            return false;
        }
    }

    async addAssignInterface(token: string, username: string, idElement: string): Promise<boolean> {
        try {
            const response = await AdminRequest.addAssignElement(token, username, idElement);
            if (response instanceof ErrorRequest) throw response;
            return true;
        } catch(error) {
            console.error(error);
            return false;
        }
    }

    async updateName(token: string, username: string, new_name: string): Promise<boolean> {
        try {
            const response = await AdminRequest.updateName(token, username, new_name);
            if (response instanceof ErrorRequest) throw response;
            return true;
        } catch(error) {
            console.error(error);
            return false;
        }
    }

    async updateLastname(token:string, username: string, new_lastname): Promise<boolean> {
        try {
            const response = await AdminRequest.updateLastname(token, username, new_lastname);
            if (response instanceof ErrorRequest) throw response;
            return true;
        } catch(error) {
            console.error(error);
            return false;
        }
    }

    async updatePassword(token: string, username: string, new_password:string): Promise<boolean> {
        try {
            const response = await AdminRequest.updatePassword(token, username, new_password);
            if (response instanceof ErrorRequest) throw response;
            return true;
        } catch(error) {
            console.error(error);
            return false;
        }
    }

    async allowChangePassword(token: string, username: string): Promise<boolean> {
        try {
            const res = AdminRequest.permissionChangePassword(token, username, "true");
            if (res instanceof ErrorRequest) throw res;
            return true;
        } catch (error) {
            console.error(error);
            return false;
        }
    }

    async denyChangePassword(token: string, username: string): Promise<boolean> {
        try {
            const res = AdminRequest.permissionChangePassword(token, username, "false");
            if (res instanceof ErrorRequest) throw res;
            return true;
        } catch (error) {
            console.error(error);
            return false;
        }
    }

    getTotalInterfaceReviewedInTheMonth(users: UserModel[]): string {
        let total = 0;
        users.map((user: UserModel) => {
            user.assigned.map((dataInterface: InterfaceModel) => {
                if (dataInterface.assignment.reviewMonth) {
                    let month = dataInterface.assignment.reviewMonth;
                    if (month == getCurrentMonth()) total = total + 1;
                }
            });
        })
        return total.toString();
    }

    getTotalInterfaceReviewedInTheDay(users: UserModel[]): string {
        let total = 0;
        users.map((user: UserModel) => {
            user.assigned.map((dataInterface: InterfaceModel) => {
                if (dataInterface.assignment.reviewMonth) {
                    let date = `${dataInterface.assignment.reviewDay}-${dataInterface.assignment.reviewMonth}-${dataInterface.assignment.reviewYear}`;
                    if (date == getCurrentDate()) total = total + 1;
                }
            });
        })
        return total.toString();
    }

    getTotalInterfacePending(users: UserModel[]): string {
        let total = 0;
        users.map((user: UserModel) => {
            user.assigned.map((dataInterface: InterfaceModel) => {
                if (dataInterface.assignment.status == assignmentStatus.pending) total = total + 1;
            });
        })
        return total.toString();
    }

    getMonthsOfUserData(users: UserModel[]): Array<{"monthString": string, "monthNumber": string}> {
        let monthsData: Array<{"monthString": string, "monthNumber": string}> = [];
        users.map((user: UserModel) => {
            user.assigned.map((dataInterface: InterfaceModel) => {
                if (dataInterface.assignment.reviewMonth) {
                    let interfaceMonth = dataInterface.assignment.reviewMonth;
                    if (!monthsData.some(month => month.monthNumber === interfaceMonth)) {
                        monthsData.push({
                            "monthString": months[Number(interfaceMonth) - 1],
                            "monthNumber": interfaceMonth
                        });
                    }
                }
            });
        });
        return monthsData;
    }

    getUsersWithInterfacesReviewedInTheMonth(users: UserModel[], month: string): UserModel[] {
        let usersFilter: UserModel[] = [];
        let addUsers = {};
        users.map((user: UserModel) => {
            if (!addUsers[user.username]) {
                user.assigned.map((dataInterface: InterfaceModel) => {
                    let interfaceMonth = dataInterface.assignment.reviewMonth;
                    if ((!addUsers[user.username]) && (interfaceMonth === month)) {
                        usersFilter.push(user);
                        addUsers[user.username] = true;
                    }
                });
            }
        })
        return usersFilter;        
    }
}

export const AdminController = new ControllerAdmin();