import { InterfaceAssignedSchema, InterfaceChangeSchema } from '@/schemas/interface';
import { AssignmentStatusTypes } from '@/constants/types';
import * as ExcelJS from 'exceljs';

export class ExportHandler {
    static async exportHistoryUserToExcel(username: string, interfaces: InterfaceAssignedSchema[]): Promise<string | null> {
        try {
            const workbook = new ExcelJS.Workbook();
            const worksheet = workbook.addWorksheet(`Historial de ${username}`);

            worksheet.columns = [
                { header: 'Fecha de Asignación', key: 'dateAssignment', width: 30 },
                { header: 'Asignado por', key: 'assignedBy', width: 30 },
                { header: 'Estatus Asignación', key: 'status', width: 30 },
                { header: 'Fecha de Realización', key: 'updateAt', width: 30 },
                { header: 'IP', key: 'ip', width: 30 },
                { header: 'Community', key: 'community', width: 30 },
                { header: 'Sysname', key: 'sysname', width: 30 },
                { header: 'ifIndex', key: 'ifIndex', width: 30 },
                { header: 'ifName Antiguo', key: 'ifNameOld', width: 30 },
                { header: 'ifName Actual', key: 'ifNameNew', width: 30 },
                { header: 'ifDescr Antiguo', key: 'ifDescrOld', width: 30 },
                { header: 'ifDescr Actual', key: 'ifDescrNew', width: 30 },
                { header: 'ifAlias Antiguo', key: 'ifAliasOld', width: 30 },
                { header: 'ifAlias Actual', key: 'ifAliasNew', width: 30 },
                { header: 'ifHighSpeed Antiguo', key: 'ifHighSpeedOld', width: 30 },
                { header: 'ifHighSpeed Actual', key: 'ifHighSpeedNew', width: 30 },
                { header: 'ifOperStatus Antiguo', key: 'ifOperStatusOld', width: 30 },
                { header: 'ifOperStatus Actual', key: 'ifOperStatusNew', width: 30 },
                { header: 'ifAdminStatus Antiguo', key: 'ifAdminStatusOld', width: 30 },
                { header: 'ifAdminStatus Actual', key: 'ifAdminStatusNew', width: 30 },
            ];

            interfaces.forEach((assignment) => {
                let statusTranslation: string = '';
                if (assignment.type_status === AssignmentStatusTypes.PENDING) statusTranslation = "Pendiente"
                else if (assignment.type_status === AssignmentStatusTypes.INSPECTED) statusTranslation = "Revisado";
                else if (assignment.type_status === AssignmentStatusTypes.REDISCOVERED) statusTranslation = "Revisado (Interfaz Redescubierta)"
                worksheet.addRow({
                    dateAssignment: assignment.created_at,
                    assignedBy: assignment.assign_by,
                    status: statusTranslation,
                    assignedTo: username,
                    ip: assignment.ip_new,
                    community: assignment.community_new,
                    sysname: assignment.sysname_new,
                    ifIndex: assignment.ifIndex_new,
                    ifNameOld: assignment.ifName_old,
                    ifNameNew: assignment.ifName_new,
                    ifDescrOld: assignment.ifDescr_old,
                    ifDescrNew: assignment.ifDescr_new,
                    ifAliasOld: assignment.ifAlias_old,
                    ifAliasNew: assignment.ifAlias_new,
                    ifHighSpeedOld: assignment.ifHighSpeed_old,
                    ifHighSpeedNew: assignment.ifHighSpeed_new,
                    ifOperStatusOld: assignment.ifOperStatus_old,
                    ifOperStatusNew: assignment.ifOperStatus_new,
                    ifAdminStatusOld: assignment.ifAdminStatus_old,
                    ifAdminStatusNew: assignment.ifAdminStatus_new
                });
            });

            const buffer = await workbook.xlsx.writeBuffer();
            const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
            const url = window.URL.createObjectURL(blob);
            return url;
        } catch (error) {
            console.error(error);
            return null;
        }
    }

    static async exportInterfaceChangesToExcel(interfaces: InterfaceChangeSchema[]): Promise<string | null> {
        try {
            const workbook = new ExcelJS.Workbook();
            const worksheet = workbook.addWorksheet(`Cambios de Interfaces`);

            worksheet.columns = [
                { header: 'IP', key: 'ip', width: 30 },
                { header: 'Community', key: 'community', width: 30 },
                { header: 'Sysname', key: 'sysname', width: 30 },
                { header: 'ifIndex', key: 'ifIndex', width: 30 },
                { header: 'ifName Antiguo', key: 'ifNameOld', width: 30 },
                { header: 'ifName Actual', key: 'ifNameNew', width: 30 },
                { header: 'ifDescr Antiguo', key: 'ifDescrOld', width: 30 },
                { header: 'ifDescr Actual', key: 'ifDescrNew', width: 30 },
                { header: 'ifAlias Antiguo', key: 'ifAliasOld', width: 30 },
                { header: 'ifAlias Actual', key: 'ifAliasNew', width: 30 },
                { header: 'ifHighSpeed Antiguo', key: 'ifHighSpeedOld', width: 30 },
                { header: 'ifHighSpeed Actual', key: 'ifHighSpeedNew', width: 30 },
                { header: 'ifOperStatus Antiguo', key: 'ifOperStatusOld', width: 30 },
                { header: 'ifOperStatus Actual', key: 'ifOperStatusNew', width: 30 },
                { header: 'ifAdminStatus Antiguo', key: 'ifAdminStatusOld', width: 30 },
                { header: 'ifAdminStatus Actual', key: 'ifAdminStatusNew', width: 30 },
                { header: 'Asignado a', key: 'assignedTo', width: 30 },
            ];

            interfaces.forEach((assignment) => {
                worksheet.addRow({
                    ip: assignment.ip_new,
                    community: assignment.community_new,
                    sysname: assignment.sysname_new,
                    ifIndex: assignment.ifIndex_new,
                    ifNameOld: assignment.ifName_old,
                    ifNameNew: assignment.ifName_new,
                    ifDescrOld: assignment.ifDescr_old,
                    ifDescrNew: assignment.ifDescr_new,
                    ifAliasOld: assignment.ifAlias_old,
                    ifAliasNew: assignment.ifAlias_new,
                    ifHighSpeedOld: assignment.ifHighSpeed_old,
                    ifHighSpeedNew: assignment.ifHighSpeed_new,
                    ifOperStatusOld: assignment.ifOperStatus_old,
                    ifOperStatusNew: assignment.ifOperStatus_new,
                    ifAdminStatusOld: assignment.ifAdminStatus_old,
                    ifAdminStatusNew: assignment.ifAdminStatus_new,
                    assignedTo: assignment.username ?? "No Asignado"
                });
            });

            const buffer = await workbook.xlsx.writeBuffer();
            const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
            const url = window.URL.createObjectURL(blob);
            return url;
        } catch (error) {
            console.error(error);
            return null;
        }
    }
}