import type { AssignmentStatusModel } from "../models/assignStatus";
import { assignmentStatus } from "../../constants/assigmentStatus";
import { getCurrentMonth, getCurrentDate } from "../../utils/date";
import type { InterfaceModel } from "../models/interface";
import { UserRequest } from "../handlers/user.handler";
import type { UserModel } from "../models/user";
import { ErrorRequest } from "../class/Error";
import * as XLSX from 'xlsx';

class ControllerUser {

    async getData(token: string, username: string): Promise<UserModel> {
        try {
            const response = await UserRequest.getDataUser(token, username);
            if (response instanceof ErrorRequest) throw response;
            return response;
        } catch (error) {
            console.error(error);
            return null;
        }
    }

    async updateAssignment(token: string, username: string, idElement: string, option: string) {
        try {
            let assignmentStatus: AssignmentStatusModel = {
                "username": username,
                "idElement": idElement,
                "status": option
            }
            const response = await UserRequest.updateAssignment(token, assignmentStatus);
            if (response instanceof ErrorRequest) throw response;
            return true;
        } catch (error) {
            console.error(error);
            return false;
        }
    }

    async updateName(token: string, username: string, new_name: string): Promise<boolean> {
        try {
            const response = await UserRequest.updateName(token, username, new_name);
            if (response instanceof ErrorRequest) throw response;
            return true;
        } catch (error) {
            console.error(error);
            return false;
        }
    }

    async updateLastname(token: string, username: string, new_lastname: string): Promise<boolean> {
        try {
            const response = await UserRequest.updateLastname(token, username, new_lastname);
            if (response instanceof ErrorRequest) throw response;
            return true;
        } catch (error) {
            console.error(error);
            return false;
        }
    }

    async updatePassword(token: string, username: string, new_password: string): Promise<boolean> {
        try {
            const response = await UserRequest.updatePassword(token, username, new_password);
            if (response instanceof ErrorRequest) throw response;
            return true;
        } catch (error) {
            console.error(error);
            return false;
        }
    }

    getTotalInterfaceReviewedInTheMonth(user: UserModel): string {
        let total = 0;
        user.assigned.map((dataInterface: InterfaceModel) => {
            if (dataInterface.assignment.reviewMonth) {
                let month = dataInterface.assignment.reviewMonth;
                if (month == getCurrentMonth()) total = total + 1;
            }
        });
        return total.toString();
    }

    getTotalInterfaceReviewedInTheDay(user: UserModel): string {
        let total = 0;
        user.assigned.map((dataInterface: InterfaceModel) => {
            if ((dataInterface.assignment.reviewDay) && (dataInterface.assignment.reviewMonth) && (dataInterface.assignment.reviewYear)) {
                let date = `${dataInterface.assignment.reviewDay}-${dataInterface.assignment.reviewMonth}-${dataInterface.assignment.reviewYear}`;
                if (date == getCurrentDate()) total = total + 1;
            }
        });
        return total.toString();
    }

    getTotalInterfacePending(user: UserModel): string {
        let total = 0;
        user.assigned.map((dataInterface: InterfaceModel) => {
            if (dataInterface.assignment.status == assignmentStatus.pending) total = total + 1;
        });
        return total.toString();
    }

    getTotalInterfacePendingInTheMonth(user: UserModel): string {
        let total = 0;
        user.assigned.map((dataInterface: InterfaceModel) => {
            if (dataInterface.assignment.status == assignmentStatus.pending) {
                let interfaceMonth = dataInterface.assignment.assignedDate.split('-')[1];
                if (interfaceMonth == getCurrentMonth()) total = total + 1;
            }
        });
        return total.toString();
    }

    getTotalInterfacePendingInTheDay(user: UserModel): string {
        let total = 0;
        user.assigned.map((dataInterface: InterfaceModel) => {
            if ((dataInterface.assignment.status == assignmentStatus.pending) 
                && (dataInterface.assignment.assignedDate == getCurrentDate())) total = total + 1; 
        });
        return total.toString();
    }

    getTotalInterfaceAssignedInTheMonth(user: UserModel): string {
        let total = 0;
        user.assigned.map((dataInterface: InterfaceModel) => {
            let interfaceMonth = dataInterface.assignment.assignedDate.split('-')[1];
            if (interfaceMonth == getCurrentMonth()) total = total + 1;
        });
        return total.toString();
    }

    getTotalInterfaceAssignedInTheDay(user: UserModel): string {
        let total = 0;
        user.assigned.map((dataInterface: InterfaceModel) => {
            let interfaceMonth = dataInterface.assignment.assignedDate;
            if (interfaceMonth == getCurrentDate()) total = total + 1;
        });
        return total.toString();
    }

    getInterfacesPending(user: UserModel): InterfaceModel[] {
        let interfacesPending: InterfaceModel[] = [];
        user.assigned.map((dataInterface: InterfaceModel) => {
            if (dataInterface.assignment.status == assignmentStatus.pending) interfacesPending.push(dataInterface);
        });
        return interfacesPending;
    }

    getInterfacesReviewed(user: UserModel): InterfaceModel[] {
        let interfacesReviewed: InterfaceModel[] = [];
        user.assigned.map((dataInterface: InterfaceModel) => {
            if ((dataInterface.assignment.status != assignmentStatus.pending)
                && (dataInterface.assignment.status != assignmentStatus.default)) interfacesReviewed.push(dataInterface);
        });
        return interfacesReviewed;
    }

    async generateDataToExcelOfInterfaceReviewed(dataInterfaces: InterfaceModel[], month?: string): Promise<void> {
        let data = []
        if (!month) {
            dataInterfaces.map((dataInterface: InterfaceModel) => {
                if (dataInterface.assignment.reviewMonth) {
                    data.push({
                        "IP": dataInterface.ip,
                        "Comunidad": dataInterface.community,
                        "Fecha de Asignación de Revisión": dataInterface.assignment.assignedDate,
                        "Fecha de Revisión": `${dataInterface.assignment.reviewDay}-${dataInterface.assignment.reviewMonth}-${dataInterface.assignment.reviewYear}`,
                        "Estatus de Revisión": dataInterface.assignment.status,
                        "Asignado a": dataInterface.assignment.usernameAssigned
                    })
                } 
            });
        } else {
            dataInterfaces.map((dataInterface: InterfaceModel) => {
                if (dataInterface.assignment.reviewMonth) {
                    let interfaceMonth = dataInterface.assignment.reviewMonth;
                    if (interfaceMonth == month) {
                        data.push({
                            "IP": dataInterface.ip,
                            "Comunidad": dataInterface.community,
                            "Fecha de Asignación de Revisión": dataInterface.assignment.assignedDate,
                            "Fecha de Revisión": `${dataInterface.assignment.reviewDay}-${dataInterface.assignment.reviewMonth}-${dataInterface.assignment.reviewYear}`,
                            "Estatus de Revisión": dataInterface.assignment.status,
                            "Asignado a": dataInterface.assignment.usernameAssigned
                        })
                    } 
                }
            });
        }
        const workbook = XLSX.utils.book_new();
        const worksheet = XLSX.utils.json_to_sheet(data);
        worksheet["!cols"] = [
            { wpx: 100 },
            { wpx: 100 },
            { wpx: 120 },
            { wpx: 120 },
            { wpx: 120 },
            { wpx: 120 },
            { wpx: 120 },
            { wpx: 120 },
            { wpx: 120 },
            { wpx: 120 },
            { wpx: 120 },
            { wpx: 120 },
            { wpx: 120 },
            { wpx: 120 },
            { wpx: 120 },
        ]
        
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Interfaces');
        XLSX.writeFile(workbook, `Historial.xlsx`);
    }

}

export const UserController = new ControllerUser();