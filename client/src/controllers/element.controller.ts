import { ElementRequest } from "../handlers/element.handler";
import { getCurrentMonth } from "../../utils/date";
import type { Element } from '../models/element';
import { ErrorRequest } from "../class/Error";
import * as XLSX from 'xlsx';

class ControllerElement {
    private refactorElements (elements: Element[]): Element[] {
        let refactorElements: Element[] = [];
        elements.map((element: Element) => {
            if (element.old.community.includes("*e*")) element.old.community = element.old.community.replace("*e*", "\\");
            if (element.old.ifName.includes("*e*")) element.old.ifName = element.old.ifName.replace("*e*", "\\");
            if (element.old.ifDescr.includes("*e*")) element.old.ifDescr = element.old.ifDescr.replace("*e*", "\\");
            if (element.old.ifAlias.includes("*e*")) element.old.ifAlias = element.old.ifAlias.replace("*e*", "\\");
            if (element.old.ifHighSpeed.includes("*e*")) element.old.ifHighSpeed = element.old.ifHighSpeed.replace("*e*", "\\");
            if (element.old.ifOperStatus.includes("*e*")) element.old.ifOperStatus = element.old.ifOperStatus.replace("*e*", "\\");
            if (element.old.ifAdminStatus.includes("*e*")) element.old.ifAdminStatus = element.old.ifAdminStatus.replace("*e*", "\\");
            if (element.current.community.includes("*e*")) element.current.community = element.current.community.replace("*e*", "\\");
            if (element.current.ifName.includes("*e*")) element.current.ifName = element.current.ifName.replace("*e*", "\\");
            if (element.current.ifDescr.includes("*e*")) element.current.ifDescr = element.current.ifDescr.replace("*e*", "\\");
            if (element.current.ifAlias.includes("*e*")) element.current.ifAlias = element.current.ifAlias.replace("*e*", "\\");
            if (element.current.ifHighSpeed.includes("*e*")) element.current.ifHighSpeed = element.current.ifHighSpeed.replace("*e*", "\\");
            if (element.current.ifOperStatus.includes("*e*")) element.current.ifOperStatus = element.current.ifOperStatus.replace("*e*", "\\");
            if (element.current.ifAdminStatus.includes("*e*")) element.current.ifAdminStatus = element.current.ifAdminStatus.replace("*e*", "\\");
            refactorElements.push(element);
        });
        return refactorElements;
    }

    private refactorElement (element: Element): Element {
        if (element.old.community.includes("*e*")) element.old.community = element.old.community.replace("*e*", "\\");
        if (element.old.ifName.includes("*e*")) element.old.ifName = element.old.ifName.replace("*e*", "\\");
        if (element.old.ifDescr.includes("*e*")) element.old.ifDescr = element.old.ifDescr.replace("*e*", "\\");
        if (element.old.ifAlias.includes("*e*")) element.old.ifAlias = element.old.ifAlias.replace("*e*", "\\");
        if (element.old.ifHighSpeed.includes("*e*")) element.old.ifHighSpeed = element.old.ifHighSpeed.replace("*e*", "\\");
        if (element.old.ifOperStatus.includes("*e*")) element.old.ifOperStatus = element.old.ifOperStatus.replace("*e*", "\\");
        if (element.old.ifAdminStatus.includes("*e*")) element.old.ifAdminStatus = element.old.ifAdminStatus.replace("*e*", "\\");
        if (element.current.community.includes("*e*")) element.current.community = element.current.community.replace("*e*", "\\");
        if (element.current.ifName.includes("*e*")) element.current.ifName = element.current.ifName.replace("*e*", "\\");
        if (element.current.ifDescr.includes("*e*")) element.current.ifDescr = element.current.ifDescr.replace("*e*", "\\");
        if (element.current.ifAlias.includes("*e*")) element.current.ifAlias = element.current.ifAlias.replace("*e*", "\\");
        if (element.current.ifHighSpeed.includes("*e*")) element.current.ifHighSpeed = element.current.ifHighSpeed.replace("*e*", "\\");
        if (element.current.ifOperStatus.includes("*e*")) element.current.ifOperStatus = element.current.ifOperStatus.replace("*e*", "\\");
        if (element.current.ifAdminStatus.includes("*e*")) element.current.ifAdminStatus = element.current.ifAdminStatus.replace("*e*", "\\");
        return element;
    }

    async getElementsToday(token: string): Promise<Element[] | null> {
        try {
            const response = await ElementRequest.getElementsToday(token);
            if (response instanceof ErrorRequest) throw response;
            let elements: Element[] = this.refactorElements(response);
            return elements;
        } catch (error) {
            console.error(error);
            return null;
        }
    }

    async getElements(token: string): Promise<Element[] | null> {
        try {
            const response = await ElementRequest.getElements(token);
            if (response instanceof ErrorRequest) throw response;
            let elements: Element[] = this.refactorElements(response);
            return elements;
        } catch(error) {
            console.error(error);
            return null;
        }
    }

    async getElementsByUser(token: string, username: string): Promise<Element[]> {
        try {
            let elementsUser: Element[] = [];
            const response = await ElementRequest.getElements(token);
            if (response instanceof ErrorRequest) throw response;
            let elements: Element[] = this.refactorElements(response);
            elements.map((element: Element) => {
                if (element.assignment.usernameAssigned == username) elementsUser.push(element);
            })
            return elementsUser;
        } catch(error) {
            console.error(error);
            return null;
        }
    }

    async getElement(token: string, id: string): Promise<Element | null> {
        try {
            const response = await ElementRequest.getElement(token, id);
            if (response instanceof ErrorRequest) throw response;
            let element: Element = this.refactorElement(response);
            return element;
        } catch (error) {
            console.error(error);
            return null;
        }
    }

    async generateDataToExcel(elements: Element[], date?: string): Promise<void> {
        let data = []
        if (!date) {
            elements.map((element: Element) => {
                if (element.assignment.isAssigned == "false") {
                    data.push({
                        "Fecha de la Data": element.date,
                        "IP": element.current.ip,
                        "Comunidad": element.current.community,
                        "Nombre Antiguo": element.old.ifName,
                        "Nombre Actual": element.current.ifName,
                        "Alias Antiguo": element.old.ifAlias,
                        "Alias Actual": element.current.ifAlias,
                        "Descripción Antigua": element.old.ifDescr,
                        "Descripción Actual": element.current.ifDescr,
                        "Velocidad Antigua": element.old.ifHighSpeed,
                        "Velocidad Actual": element.current.ifHighSpeed,
                        "Operación Antigua": element.old.ifOperStatus,
                        "Operación Actual": element.current.ifOperStatus,
                        "Administración Antigua": element.old.ifAdminStatus,
                        "Administración Actual": element.current.ifAdminStatus,
                        "Estatus de Asignación": "Sin asignar"
                    })
                } else {
                    data.push({
                        "Fecha de la Data": element.date,
                        "IP": element.current.ip,
                        "Comunidad": element.current.community,
                        "Nombre Antiguo": element.old.ifName,
                        "Nombre Actual": element.current.ifName,
                        "Alias Antiguo": element.old.ifAlias,
                        "Alias Actual": element.current.ifAlias,
                        "Descripción Antigua": element.old.ifDescr,
                        "Descripción Actual": element.current.ifDescr,
                        "Velocidad Antigua": element.old.ifHighSpeed,
                        "Velocidad Actual": element.current.ifHighSpeed,
                        "Operación Antigua": element.old.ifOperStatus,
                        "Operación Actual": element.current.ifOperStatus,
                        "Administración Antigua": element.old.ifAdminStatus,
                        "Administración Actual": element.current.ifAdminStatus,
                        "Estatus de Asignación": "Asignado",
                        "Asignado a": element.assignment.usernameAssigned
                    })
                }
            });
        } else {
            elements.map((element: Element) => {
                if (element.date == date) {
                    if (element.assignment.isAssigned == "false") {
                        data.push({
                            "Fecha de la Data": element.date,
                            "IP": element.current.ip,
                            "Comunidad": element.current.community,
                            "Nombre Antiguo": element.old.ifName,
                            "Nombre Actual": element.current.ifName,
                            "Alias Antiguo": element.old.ifAlias,
                            "Alias Actual": element.current.ifAlias,
                            "Descripción Antigua": element.old.ifDescr,
                            "Descripción Actual": element.current.ifDescr,
                            "Velocidad Antigua": element.old.ifHighSpeed,
                            "Velocidad Actual": element.current.ifHighSpeed,
                            "Operación Antigua": element.old.ifOperStatus,
                            "Operación Actual": element.current.ifOperStatus,
                            "Administración Antigua": element.old.ifAdminStatus,
                            "Administración Actual": element.current.ifAdminStatus,
                            "Estatus de Asignación": "Sin asignar"
                        })
                    } else {
                        data.push({
                            "Fecha de la Data": element.date,
                            "IP": element.current.ip,
                            "Comunidad": element.current.community,
                            "Nombre Antiguo": element.old.ifName,
                            "Nombre Actual": element.current.ifName,
                            "Alias Antiguo": element.old.ifAlias,
                            "Alias Actual": element.current.ifAlias,
                            "Descripción Antigua": element.old.ifDescr,
                            "Descripción Actual": element.current.ifDescr,
                            "Velocidad Antigua": element.old.ifHighSpeed,
                            "Velocidad Actual": element.current.ifHighSpeed,
                            "Operación Antigua": element.old.ifOperStatus,
                            "Operación Actual": element.current.ifOperStatus,
                            "Administración Antigua": element.old.ifAdminStatus,
                            "Administración Actual": element.current.ifAdminStatus,
                            "Estatus de Asignación": "Asignado",
                            "Asignado a": element.assignment.usernameAssigned
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
            { wpx: 120 },
            { wpx: 120 },
        ]
        
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Data');
        XLSX.writeFile(workbook, 'DatosActuales.xlsx');
    }

    async getTotalBackup(token: string): Promise<string> {
        try {
            const response = await ElementRequest.getElements(token);
            if (response instanceof ErrorRequest) throw response;
            else {
                return response.length.toString()
            }
        } catch(error) {
            console.error(error);
            return "0";
        }
    }

    async getTotalBackupInTheMonth(token: string): Promise<string> {
        try {
            const response = await ElementRequest.getElements(token);
            if (response instanceof ErrorRequest) throw response;
            else {
                let total = 0;
                response.map((element: Element) => {
                    let interfaceMonth = element.date.split('-')[1];
                    if (interfaceMonth == getCurrentMonth()) total = total + 1;
                })
                return total.toString();
            }
        } catch(error) {
            console.error(error);
            return "0";
        }
    }

}

export const ElementController = new ControllerElement();