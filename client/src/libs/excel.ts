import { StatusAssignment, StatusAssignmentTranslation } from "./types";
import { AssignmentInfoResponseSchema } from "@/schemas/assignment";
import * as XLSX from 'xlsx';

export class ExcelHandler {
    /**
     * Generate an excel file with the historial of the user.
     * 
     * @param {string} username Username of the user.
     * @param {AssignmentInfoResponseSchema[]} history Data of assignments of the user.
     * @return {boolean} The status of the completion of the requested operation.
     */
    static getHistoryOfUser(username: string, history: AssignmentInfoResponseSchema[]): boolean {
        try {
            let dataExcel: any[] = [];
            history.map((assignment: AssignmentInfoResponseSchema) => {
                let statusTranslation: string = '';
                if (assignment.statusAssignment === StatusAssignment.pending) statusTranslation = StatusAssignmentTranslation.pending;
                else if (assignment.statusAssignment === StatusAssignment.inspected) statusTranslation = StatusAssignmentTranslation.inspected;
                else if (assignment.statusAssignment === StatusAssignment.rediscovered) statusTranslation = StatusAssignmentTranslation.rediscovered;
                dataExcel.push({
                    'Fecha de Asignación': assignment.dateAssignment,
                    'Asignado por': assignment.assignedBy,
                    'Estatus Asignación': statusTranslation,
                    'Asignado a': username,
                    'Fecha de Realización': assignment.updateAt,
                    'IP': assignment.ip,
                    'Community': assignment.community,
                    'Sysname': assignment.sysname,
                    'ifIndex': assignment.ifIndex,
                });
            });

            const workbook = XLSX.utils.book_new();
            const worksheet = XLSX.utils.json_to_sheet(dataExcel);
            worksheet["!cols"] = [
                { wpx: 100 },
                { wpx: 100 },
                { wpx: 120 },
                { wpx: 120 },
                { wpx: 120 },
                { wpx: 120 },
                { wpx: 120 },
                { wpx: 120 },
                { wpx: 120 }
            ]
            
            XLSX.utils.book_append_sheet(workbook, worksheet, `Historial de ${username}`);
            XLSX.writeFile(workbook, `${username}_historial_indices.xlsx`);
            return true;
        } catch (error) {
            console.error(error);
            return false;
        }
    }
}