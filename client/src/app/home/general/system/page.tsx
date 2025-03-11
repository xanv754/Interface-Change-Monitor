'use client';

import LoadingModal from "@app/components/modals/loading";
import AlertModal from "@app/components/modals/alert";
import Navbar from "@app/components/navbar/navbar";
import PageTitles from "@app/components/titles/titlePage";
import { CurrentSession } from "@libs/session";
import { ConfigurationService } from "@/services/configuration";
import { ConfigurationResponseSchema } from "@schemas/configuration";
import { useEffect, useState } from "react";

export default function ConfigurationGeneralView() {
    const [loading, setLoading] = useState<boolean>(true);
    const [errorInfo, setErrorInfo] = useState<boolean>(false);
    const [errorUpdate, setErrorUpdate] = useState<boolean>(false);
    const [successUpdate, setSuccessUpdate] = useState<boolean>(false);

    const [token, setToken] = useState<string | null>(null);
    const [canEdit, setCanEdit] = useState<boolean>(false);
    const [config, setConfig] = useState<ConfigurationResponseSchema | null>(null);

    const [canAssignStandard, setCanAssignStandard] = useState<boolean>(false);
    const [canAssignAdmin, setCanAssignAdmin] = useState<boolean>(false);
    const [canReceiveAssignmentStandard, setCanReceiveAssignmentStandard] = useState<boolean>(false);
    const [canReceiveAssignmentAdmin, setCanReceiveAssignmentAdmin] = useState<boolean>(false);
    const [canReceiveAssignmentRoot, setCanReceiveAssignmentRoot] = useState<boolean>(false);
    const [systemInformationStandard, setSystemInformationStandard] = useState<boolean>(false);
    const [systemInformationAdmin, setSystemInformationAdmin] = useState<boolean>(false);
    const [notificationIfName, setNotificationIfName] = useState<boolean>(false);
    const [notificationIfDescr, setNotificationIfDescr] = useState<boolean>(false);
    const [notificationIfAlias, setNotificationIfAlias] = useState<boolean>(false);
    const [notificationIfHighSpeed, setNotificationIfHighSpeed] = useState<boolean>(false);
    const [notificationIfOperStatus, setNotificationIfOperStatus] = useState<boolean>(false);
    const [notificationIfAdminStatus, setNotificationIfAdminStatus] = useState<boolean>(false);

    /**
     * Get the information of the configuration system.
     */
    const getData = async () => {
        const currentToken = CurrentSession.getToken();
        if (currentToken) {
            setToken(currentToken);
            const data = await ConfigurationService.getConfiguration(currentToken);
            if (data) {
                setConfig(data);
                setCanAssignStandard(data.canAssign.STANDARD);
                setCanAssignAdmin(data.canAssign.ADMIN);
                setCanReceiveAssignmentStandard(data.canReceiveAssignment.STANDARD);
                setCanReceiveAssignmentAdmin(data.canReceiveAssignment.ADMIN);
                setCanReceiveAssignmentRoot(data.canReceiveAssignment.ROOT);
                setSystemInformationStandard(data.systemInformation.STANDARD);
                setSystemInformationAdmin(data.systemInformation.ADMIN);
                setNotificationIfName(data.notificationChanges.ifName);
                setNotificationIfDescr(data.notificationChanges.ifDescr);
                setNotificationIfAlias(data.notificationChanges.ifAlias);
                setNotificationIfHighSpeed(data.notificationChanges.ifHighSpeed);
                setNotificationIfOperStatus(data.notificationChanges.ifOperStatus);
                setNotificationIfAdminStatus(data.notificationChanges.ifAdminStatus);
                handlerLoading(false);
            }
            else {
                handlerLoading(false);
                handlerErrorInfo(true);
            }
        }
        else {
            handlerLoading(false);
            handlerErrorInfo(true);
        }
    }

    /**
     * Update the setting of the system.
     */
    const updateSettings = async () => {
        handlerLoading(true);
        if (token) {
            let newConfig: ConfigurationResponseSchema = {
                canAssign: {
                    ROOT: true,
                    ADMIN: canAssignAdmin,
                    STANDARD: canAssignStandard,
                    SOPORT: true,
                },
                canReceiveAssignment: {
                    ROOT: canReceiveAssignmentRoot,
                    ADMIN: canReceiveAssignmentAdmin,
                    STANDARD: canReceiveAssignmentStandard,
                    SOPORT: false,
                },
                systemInformation: {
                    ROOT: true,
                    ADMIN: systemInformationAdmin,
                    STANDARD: systemInformationStandard,
                    SOPORT: true,
                },
                notificationChanges: {
                    ifName: notificationIfName,
                    ifDescr: notificationIfDescr,
                    ifAlias: notificationIfAlias,
                    ifHighSpeed: notificationIfHighSpeed,
                    ifOperStatus: notificationIfOperStatus,
                    ifAdminStatus: notificationIfAdminStatus,
                }
            }
            const status = await ConfigurationService.updateConfiguration(token, newConfig);
            if (status) {
                CurrentSession.saveConfig(newConfig);
                handlerLoading(false);
                handlerSuccessUpdate(true);
            } else {
                handlerLoading(false);
                handlerErrorUpdate(true);
            }
        } else {
            handlerLoading(false);
            handlerErrorUpdate(true);
        }
    }

    /**
     * Handler to disable the display of the loading modal.
     * 
     * @param {boolean} displayModal If the loading modal is displayed or not.
     */
    const handlerLoading = (displayModal: boolean = false) => {
        setTimeout(() => {
            setLoading(displayModal);
        }, 1000);
    }

    /**
     * Handler for user error information status.
     * 
     * @param {boolean} isThereAnError If there is an error or not.
     */
    const handlerErrorInfo = (isThereAnError: boolean = false) => {
        setErrorInfo(isThereAnError);
    }

    /**
     * Handler for success update status of configuration.
     * 
     * @param {boolean} isThereAnError If there is an error or not.
     */
    const handlerErrorUpdate = (isThereAnError: boolean = false) => {
        setErrorUpdate(isThereAnError);
    }

    /**
     * Handler for success update status of configuration.
     * 
     * @param {boolean} isSuccess If the update is successful or not.
     */
    const handlerSuccessUpdate = (isSuccess: boolean = false) => {
        setSuccessUpdate(isSuccess);
    }

    /**
     * Handler for user can edit the configuration.
     * 
     * @param {boolean} isChecked If the user can edit the configuration or not.
     */
    const handlerCanEdit = (isChecked: boolean = false) => {
        setCanEdit(isChecked);
    }

    /**
     * Handler for setting the user can assign the standard.
     * 
     * @param {boolean} isChecked If the user can or not.
     */
    const handlerCanAssignStandard = (isChecked: boolean = false) => {
        setCanAssignStandard(isChecked);
    }

    /**
     * Handler for setting the user can assign the admin.
     * 
     * @param {boolean} isChecked If the user can or not.
     */
    const handlerCanAssignAdmin = (isChecked: boolean = false) => {
        setCanAssignAdmin(isChecked);
    }

    /**
     * Handler for setting the user receive assignment the standard.
     * 
     * @param {boolean} isChecked If the user can or not.
     */
    const handlerCanReceiveAssignmentStandard = (isChecked: boolean = false) => {
        setCanReceiveAssignmentStandard(isChecked);
    }

    /**
     * Handler for setting the user can receive assignment the admin.
     * 
     * @param {boolean} isChecked If the user can or not.
     */
    const handlerCanReceiveAssignmentAdmin = (isChecked: boolean = false) => {
        setCanReceiveAssignmentAdmin(isChecked);
    }

    /**
     * Handler for setting the user can receive assignment the root.
     * 
     * @param {boolean} isChecked If the user can or not.
     */
    const handlerCanReceiveAssignmentRoot = (isChecked: boolean = false) => {
        setCanReceiveAssignmentRoot(isChecked);
    }

    /**
     * Handler for setting the user standard can see all the system information.
     * 
     * @param {boolean} isChecked If the user can or not.
     */
    const handlerSystemInformationStandard = (isChecked: boolean = false) => {
        setSystemInformationStandard(isChecked);
    }

    /**
     * Handler for setting the user admin can see all the system information.
     * 
     * @param {boolean} isChecked If the user can or not.
     */
    const handlerSystemInformationAdmin = (isChecked: boolean = false) => {
        setSystemInformationAdmin(isChecked);
    }

    /**
     * Handler for setting the user notification ifName.
     * 
     * @param {boolean} isChecked If the active or desactive.
     */
    const handlerNotificationIfName = (isChecked: boolean = false) => {
        setNotificationIfName(isChecked);
    }

    /**
     * Handler for setting the user notification ifDescr.
     * 
     * @param {boolean} isChecked If the active or desactive.
     */
    const handlerNotificationIfDescr = (isChecked: boolean = false) => {
        setNotificationIfDescr(isChecked);
    }

    /**
     * Handler for setting the user notification ifAlias.
     * 
     * @param {boolean} isChecked If the active or desactive.
     */
    const handlerNotificationIfAlias = (isChecked: boolean = false) => {
        setNotificationIfAlias(isChecked);
    }

    /**
     * Handler for setting the user notification ifHighSpeed.
     * 
     * @param {boolean} isChecked If the active or desactive.
     */
    const handlerNotificationIfHighSpeed = (isChecked: boolean = false) => {
        setNotificationIfHighSpeed(isChecked);
    }

    /**
     * Handler for setting the user notification ifOperStatus.
     * 
     * @param {boolean} isChecked If the active or desactive.
     */
    const handlerNotificationIfOperStatus = (isChecked: boolean = false) => {
        setNotificationIfOperStatus(isChecked);
    }

    /**
     * Handler for setting the user notification ifAdminStatus.
     * 
     * @param {boolean} isChecked If the active or desactive.
     */
    const handlerNotificationIfAdminStatus = (isChecked: boolean = false) => {
        setNotificationIfAdminStatus(isChecked);
    }

    /**
     * Handler for update the settings of the system.
     */
    const handlerUpdateSettings = () => {
        updateSettings();
    }

    useEffect(() => {
        getData();
    }, []);

    return (
        <main className="w-full h-screen max-h-fit flex flex-col items-center">
            <LoadingModal showModal={loading} />
            {errorInfo && 
                <AlertModal 
                    showModal={true} 
                    title='Error al obtener información' 
                    message='Ocurrió un error al intentar obtener la configuración del sistema. Por favor, refresca la página e inténtelo de nuevo. Si el error persiste, consulte a soporte.' 
                    afterAction={handlerErrorInfo}
                />
            }
            {errorUpdate && 
                <AlertModal 
                    showModal={true} 
                    title='Error al actualizar la configuración' 
                    message='Ocurrió un error al intentar actualizar la configuración del sistema. Por favor, refresca la página e inténtelo de nuevo. Si el error persiste, consulte a soporte.' 
                    afterAction={handlerErrorUpdate}
                />
            }
            {successUpdate && 
                <AlertModal 
                    showModal={true} 
                    title='Configuración actualizada' 
                    message='La configuración del sistema ha sido actualizada con éxito. Refresca la página para ver los cambios.'
                    afterAction={handlerSuccessUpdate}
                />
            }
            <section id='header' className='w-full h-fit px-4 py-1 mb-4 flex flex-col gap-4'>
                <Navbar />
                <PageTitles />
            </section>
            {config && 
                <div id='content' className='w-full h-full p-4 bg-gray-950 flex flex-col gap-3'>
                    <section className='w-full h-fit flex flex-col items-center'>
                        {!canEdit &&
                            <button 
                                id='save-button'
                                onClick={() => {handlerCanEdit(true)}}
                                className={`h-fit bg-blue-800 px-4 py-1 rounded-full text-white-50 transition-all duration-300 ease-in-out hover:bg-green-800`}
                            >
                                    Editar Configuración
                            </button>
                        }
                        {canEdit &&
                            <div className='w-full h-fit flex flex-row items-center justify-center gap-2'>
                                <button 
                                    id='save-button'
                                    onClick={() => {handlerCanEdit(false)}}
                                    className={`h-fit bg-blue-800 px-4 py-1 rounded-full text-white-50 transition-all duration-300 ease-in-out hover:bg-red-800`}
                                >
                                        Cancelar
                                </button>
                                <button 
                                    id='save-button'
                                    onClick={handlerUpdateSettings}
                                    className={`h-fit bg-blue-800 px-4 py-1 rounded-full text-white-50 transition-all duration-300 ease-in-out hover:bg-green-800`}
                                >
                                        Guardar
                                </button>
                            </div>
                        }
                    </section>
                    <section id='content-section-header' className='w-full h-fit flex flex-row justify-center gap-2 rounded-t-md'>
                        <div id='container-can-assigned' className='w-96 h-fit bg-gray-950 py-3 flex flex-col items-center justify-center gap-2 rounded-t-md'>
                            <h2 id='title' className='text-xl text-white-55 font-bold'>Permisos Para Asignar</h2>
                            <div id='content-can-assigned' className='w-full h-fit bg-white-100 px-2 py-4 flex flex-col items-center justify-start rounded-md lg:py-6'>
                                <div id="assign-user-standard" className="w-full h-fit px-4 flex flex-row items-center justify-between gap-2">
                                    <h4>Usuario Estándar</h4>
                                    <div className='relative inline-block w-[40px] h-[24px] m-[10px]'>
                                        <input 
                                            id='assign-toggle-standard' 
                                            onClick={() => {handlerCanAssignStandard(!canAssignStandard)}} 
                                            className='bg-gray-500 hidden'
                                            type="checkbox"
                                            disabled={!canEdit}
                                        />
                                        <label 
                                            htmlFor="assign-toggle-standard" 
                                            className={`absolute ${!canEdit && !canAssignStandard ? "bg-blue-950 cursor-not-allowed": ""} ${!canEdit && canAssignStandard ? "bg-green-800 before:translate-x-[16px] cursor-not-allowed": ""} ${canEdit && canAssignStandard ? "bg-green-500 before:translate-x-[16px] cursor-pointer" : ""} ${canEdit && !canAssignStandard ? "bg-blue-800": ""} top-[0] left-[0] w-[40px] h-[24px] rounded-[34px] transition duration-300 before:content-[""] before:absolute before:w-[20px] before:h-[20px] before:rounded-[50%] before:top-[2px] before:left-[2px] drop-shadow-[1px_1px_2px_rgba(0,0,0,0.3)] before:bg-white-50 before:transition before:duration-300`}
                                        />
                                    </div>
                                </div>
                                <div id="assigned-user-admin" className="w-full h-fit px-4 flex flex-row items-center justify-between gap-2">
                                    <h4>Usuario Administrador</h4>
                                    <div className='relative inline-block w-[40px] h-[24px] m-[10px]'>
                                        <input 
                                            id='assign-toggle-admin' 
                                            onClick={() => {handlerCanAssignAdmin(!canAssignAdmin)}} 
                                            className='bg-gray-500 hidden'
                                            type="checkbox"
                                            disabled={!canEdit} 
                                        />
                                        <label 
                                            htmlFor="assign-toggle-admin" 
                                            className={`absolute ${!canEdit && !canAssignAdmin ? "bg-blue-950 cursor-not-allowed": ""} ${!canEdit && canAssignAdmin ? "bg-green-800 before:translate-x-[16px] cursor-not-allowed": ""} ${canEdit && canAssignAdmin ? "bg-green-500 before:translate-x-[16px] cursor-pointer" : ""} ${canEdit && !canAssignAdmin ? "bg-blue-800": ""} top-[0] left-[0] w-[40px] h-[24px] rounded-[34px] transition duration-300 before:content-[""] before:absolute before:w-[20px] before:h-[20px] before:rounded-[50%] before:top-[2px] before:left-[2px] drop-shadow-[1px_1px_2px_rgba(0,0,0,0.3)] before:bg-white-50 before:transition before:duration-300`}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div id='content-can-assign' className='w-96 h-fit bg-gray-950 py-3 flex flex-col items-center justify-center gap-2 rounded-t-md'>
                            <h2 id='title' className='text-xl text-white-55 font-bold'>Permisos Para Recibir Asignaciones</h2>
                            <div id='content-can-assign' className='w-full h-fit bg-white-100 px-2 py-4 flex flex-col items-center justify-start rounded-md lg:py-6'>
                                <div id="assigned-user-standard" className="w-full h-fit px-4 flex flex-row items-center justify-between gap-2">
                                    <h4>Usuario Estándar</h4>
                                    <div className='relative inline-block w-[40px] h-[24px] m-[10px]'>
                                        <input 
                                            id='assigned-toggle-standard' 
                                            onClick={() => {handlerCanReceiveAssignmentStandard(!canReceiveAssignmentStandard)}} 
                                            className='bg-gray-500 hidden'
                                            type="checkbox"
                                            disabled={!canEdit} 
                                        />
                                        <label 
                                            htmlFor="assigned-toggle-standard" 
                                            className={`absolute ${!canEdit && !canReceiveAssignmentStandard ? "bg-blue-950 cursor-not-allowed": ""} ${!canEdit && canReceiveAssignmentStandard ? "bg-green-800 before:translate-x-[16px] cursor-not-allowed": ""} ${canEdit && canReceiveAssignmentStandard ? "bg-green-500 before:translate-x-[16px] cursor-pointer" : ""} ${canEdit && !canReceiveAssignmentStandard ? "bg-blue-800": ""} top-[0] left-[0] w-[40px] h-[24px] rounded-[34px] transition duration-300 before:content-[""] before:absolute before:w-[20px] before:h-[20px] before:rounded-[50%] before:top-[2px] before:left-[2px] drop-shadow-[1px_1px_2px_rgba(0,0,0,0.3)] before:bg-white-50 before:transition before:duration-300`}
                                        />
                                    </div>
                                </div>
                                <div id="assign-user-admin" className="w-full h-fit px-4 flex flex-row items-center justify-between gap-2">
                                    <h4>Usuario Administrador</h4>
                                    <div className='relative inline-block w-[40px] h-[24px] m-[10px]'>
                                        <input 
                                            id='assigned-toggle-admin' 
                                            onClick={() => {handlerCanReceiveAssignmentAdmin(!canReceiveAssignmentAdmin)}} 
                                            className='bg-gray-500 hidden'
                                            type="checkbox"
                                            disabled={!canEdit} 
                                        />
                                        <label 
                                            htmlFor="assigned-toggle-admin" 
                                            className={`absolute ${!canEdit && !canReceiveAssignmentAdmin ? "bg-blue-950 cursor-not-allowed": ""} ${!canEdit && canReceiveAssignmentAdmin ? "bg-green-800 before:translate-x-[16px] cursor-not-allowed": ""} ${canEdit && canReceiveAssignmentAdmin ? "bg-green-500 before:translate-x-[16px] cursor-pointer" : ""} ${canEdit && !canReceiveAssignmentAdmin ? "bg-blue-800": ""} top-[0] left-[0] w-[40px] h-[24px] rounded-[34px] transition duration-300 before:content-[""] before:absolute before:w-[20px] before:h-[20px] before:rounded-[50%] before:top-[2px] before:left-[2px] drop-shadow-[1px_1px_2px_rgba(0,0,0,0.3)] before:bg-white-50 before:transition before:duration-300`}
                                        />
                                    </div>
                                </div>
                                <div id="assign-user-root" className="w-full h-fit px-4 flex flex-row items-center justify-between gap-2">
                                    <h4>Super Usuario</h4>
                                    <div className='relative inline-block w-[40px] h-[24px] m-[10px]'>
                                        <input 
                                            id='assigned-toggle-root' 
                                            onClick={() => {handlerCanReceiveAssignmentRoot(!canReceiveAssignmentRoot)}} 
                                            className='bg-gray-500 hidden'
                                            type="checkbox"
                                            disabled={!canEdit} 
                                        />
                                        <label 
                                            htmlFor="assigned-toggle-root" 
                                            className={`absolute ${!canEdit && !canReceiveAssignmentRoot ? "bg-blue-950 cursor-not-allowed": ""} ${!canEdit && canReceiveAssignmentRoot ? "bg-green-800 before:translate-x-[16px] cursor-not-allowed": ""} ${canEdit && canReceiveAssignmentRoot ? "bg-green-500 before:translate-x-[16px] cursor-pointer" : ""} ${canEdit && !canReceiveAssignmentRoot ? "bg-blue-800": ""} top-[0] left-[0] w-[40px] h-[24px] rounded-[34px] transition duration-300 before:content-[""] before:absolute before:w-[20px] before:h-[20px] before:rounded-[50%] before:top-[2px] before:left-[2px] drop-shadow-[1px_1px_2px_rgba(0,0,0,0.3)] before:bg-white-50 before:transition before:duration-300`}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div id='content-info-system' className='w-fit h-fit bg-gray-950 py-3 flex flex-col items-center justify-center gap-2 rounded-t-md'>
                            <h2 id='title' className='text-xl text-white-55 font-bold'>Permisos Para Ver y Actualizar Información del Sistema</h2>
                            <div id='content-can-assign' className='w-full h-fit bg-white-100 px-2 py-4 flex flex-col items-center justify-start rounded-md lg:py-6'>
                                <div id="info-user-standard" className="w-full h-fit px-4 flex flex-row items-center justify-between gap-2">
                                    <h4>Usuario Estándar</h4>
                                    <div className='relative inline-block w-[40px] h-[24px] m-[10px]'>
                                        <input 
                                            id='info-toggle-standard' 
                                            onClick={() => {handlerSystemInformationStandard(!systemInformationStandard)}} 
                                            className='bg-gray-500 hidden'
                                            type="checkbox"
                                            disabled={!canEdit} 
                                        />
                                        <label 
                                            htmlFor="info-toggle-standard" 
                                            className={`absolute ${!canEdit && !systemInformationStandard ? "bg-blue-950 cursor-not-allowed": ""} ${!canEdit && systemInformationStandard ? "bg-green-800 before:translate-x-[16px] cursor-not-allowed": ""} ${canEdit && systemInformationStandard ? "bg-green-500 before:translate-x-[16px] cursor-pointer" : ""} ${canEdit && !systemInformationStandard ? "bg-blue-800": ""} top-[0] left-[0] w-[40px] h-[24px] rounded-[34px] transition duration-300 before:content-[""] before:absolute before:w-[20px] before:h-[20px] before:rounded-[50%] before:top-[2px] before:left-[2px] drop-shadow-[1px_1px_2px_rgba(0,0,0,0.3)] before:bg-white-50 before:transition before:duration-300`}
                                        />
                                    </div>
                                </div>
                                <div id="info-user-admin" className="w-full h-fit px-4 flex flex-row items-center justify-between gap-2">
                                    <h4>Usuario Administrador</h4>
                                    <div className='relative inline-block w-[40px] h-[24px] m-[10px]'>
                                        <input 
                                            id='info-toggle-admin' 
                                            onClick={() => {handlerSystemInformationAdmin(!systemInformationAdmin)}} 
                                            className='bg-gray-500 hidden'
                                            type="checkbox"
                                            disabled={!canEdit} 
                                        />
                                        <label 
                                            htmlFor="info-toggle-admin" 
                                            className={`absolute ${!canEdit && !systemInformationAdmin ? "bg-blue-950 cursor-not-allowed": ""} ${!canEdit && systemInformationAdmin ? "bg-green-800 before:translate-x-[16px] cursor-not-allowed": ""} ${canEdit && systemInformationAdmin ? "bg-green-500 before:translate-x-[16px] cursor-pointer" : ""} ${canEdit && !systemInformationAdmin ? "bg-blue-800": ""} top-[0] left-[0] w-[40px] h-[24px] rounded-[34px] transition duration-300 before:content-[""] before:absolute before:w-[20px] before:h-[20px] before:rounded-[50%] before:top-[2px] before:left-[2px] drop-shadow-[1px_1px_2px_rgba(0,0,0,0.3)] before:bg-white-50 before:transition before:duration-300`}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>
                    <section id='content-section-notification' className='w-full h-fit'>
                        <div id='content-notification' className='w-full h-fit bg-gray-950 py-3 flex flex-col items-center justify-center gap-2 rounded-t-md'>
                            <h2 id='title' className='text-xl text-white-55 font-bold'>Campos para Recibir Notificaciones de Cambios</h2>
                            <div id='content-can-assign' className='w-full h-fit bg-white-100 px-2 py-4 flex flex-col items-center justify-start rounded-md lg:py-6'>
                                <div id="info-ifName" className="w-full h-fit px-4 flex flex-row items-center justify-between gap-2">
                                    <h4>ifName - Nombre de la Interfaz</h4>
                                    <div className='relative inline-block w-[40px] h-[24px] m-[10px]'>
                                        <input 
                                            id='notification-ifName' 
                                            onClick={() => {handlerNotificationIfName(!notificationIfName)}} 
                                            className='bg-gray-500 hidden'
                                            type="checkbox"
                                            disabled={!canEdit} 
                                        />
                                        <label 
                                            htmlFor="notification-ifName" 
                                            className={`absolute ${!canEdit && !notificationIfName ? "bg-blue-950 cursor-not-allowed": ""} ${!canEdit && notificationIfName ? "bg-green-800 before:translate-x-[16px] cursor-not-allowed": ""} ${canEdit && notificationIfName ? "bg-green-500 before:translate-x-[16px] cursor-pointer" : ""} ${canEdit && !notificationIfName ? "bg-blue-800": ""} top-[0] left-[0] w-[40px] h-[24px] rounded-[34px] transition duration-300 before:content-[""] before:absolute before:w-[20px] before:h-[20px] before:rounded-[50%] before:top-[2px] before:left-[2px] drop-shadow-[1px_1px_2px_rgba(0,0,0,0.3)] before:bg-white-50 before:transition before:duration-300`}
                                        />
                                    </div>
                                </div>
                                <div id="info-ifDescr" className="w-full h-fit px-4 flex flex-row items-center justify-between gap-2">
                                    <h4>ifDescr - Descripción de la Interfaz</h4>
                                    <div className='relative inline-block w-[40px] h-[24px] m-[10px]'>
                                        <input 
                                            id='notification-ifDescr' 
                                            onClick={() => {handlerNotificationIfDescr(!notificationIfDescr)}} 
                                            className='bg-gray-500 hidden'
                                            type="checkbox"
                                            disabled={!canEdit} 
                                        />
                                        <label 
                                            htmlFor="notification-ifDescr" 
                                            className={`absolute ${!canEdit && !notificationIfDescr ? "bg-blue-950 cursor-not-allowed": ""} ${!canEdit && notificationIfDescr ? "bg-green-800 before:translate-x-[16px] cursor-not-allowed": ""} ${canEdit && notificationIfDescr ? "bg-green-500 before:translate-x-[16px] cursor-pointer" : ""} ${canEdit && !notificationIfDescr ? "bg-blue-800": ""} top-[0] left-[0] w-[40px] h-[24px] rounded-[34px] transition duration-300 before:content-[""] before:absolute before:w-[20px] before:h-[20px] before:rounded-[50%] before:top-[2px] before:left-[2px] drop-shadow-[1px_1px_2px_rgba(0,0,0,0.3)] before:bg-white-50 before:transition before:duration-300`}
                                        />
                                    </div>
                                </div>
                                <div id="info-ifAlias" className="w-full h-fit px-4 flex flex-row items-center justify-between gap-2">
                                    <h4>ifAlias - Alias de la Interfaz</h4>
                                    <div className='relative inline-block w-[40px] h-[24px] m-[10px]'>
                                        <input 
                                            id='notification-ifAlias' 
                                            onClick={() => {handlerNotificationIfAlias(!notificationIfAlias)}} 
                                            className='bg-gray-500 hidden'
                                            type="checkbox"
                                            disabled={!canEdit} 
                                        />
                                        <label 
                                            htmlFor="notification-ifAlias" 
                                            className={`absolute ${!canEdit && !notificationIfAlias ? "bg-blue-950 cursor-not-allowed": ""} ${!canEdit && notificationIfAlias ? "bg-green-800 before:translate-x-[16px] cursor-not-allowed": ""} ${canEdit && notificationIfAlias ? "bg-green-500 before:translate-x-[16px] cursor-pointer" : ""} ${canEdit && !notificationIfAlias ? "bg-blue-800": ""} top-[0] left-[0] w-[40px] h-[24px] rounded-[34px] transition duration-300 before:content-[""] before:absolute before:w-[20px] before:h-[20px] before:rounded-[50%] before:top-[2px] before:left-[2px] drop-shadow-[1px_1px_2px_rgba(0,0,0,0.3)] before:bg-white-50 before:transition before:duration-300`}
                                        />
                                    </div>
                                </div>
                                <div id="info-ifHighSpeed" className="w-full h-fit px-4 flex flex-row items-center justify-between gap-2">
                                    <h4>ifHighSpeed - Capacidad de la Interfaz</h4>
                                    <div className='relative inline-block w-[40px] h-[24px] m-[10px]'>
                                        <input 
                                            id='notification-ifHighSpeed' 
                                            onClick={() => {handlerNotificationIfHighSpeed(!notificationIfHighSpeed)}} 
                                            className='bg-gray-500 hidden'
                                            type="checkbox"
                                            disabled={!canEdit} 
                                        />
                                        <label 
                                            htmlFor="notification-ifHighSpeed" 
                                            className={`absolute ${!canEdit && !notificationIfHighSpeed ? "bg-blue-950 cursor-not-allowed": ""} ${!canEdit && notificationIfHighSpeed ? "bg-green-800 before:translate-x-[16px] cursor-not-allowed": ""} ${canEdit && notificationIfHighSpeed ? "bg-green-500 before:translate-x-[16px] cursor-pointer" : ""} ${canEdit && !notificationIfHighSpeed ? "bg-blue-800": ""} top-[0] left-[0] w-[40px] h-[24px] rounded-[34px] transition duration-300 before:content-[""] before:absolute before:w-[20px] before:h-[20px] before:rounded-[50%] before:top-[2px] before:left-[2px] drop-shadow-[1px_1px_2px_rgba(0,0,0,0.3)] before:bg-white-50 before:transition before:duration-300`}
                                        />
                                    </div>
                                </div>
                                <div id="info-ifOperStatus" className="w-full h-fit px-4 flex flex-row items-center justify-between gap-2">
                                    <h4>ifOperStatus - Estatus Operativo de la Interfaz</h4>
                                    <div className='relative inline-block w-[40px] h-[24px] m-[10px]'>
                                        <input 
                                            id='notification-ifOperStatus' 
                                            onClick={() => {handlerNotificationIfOperStatus(!notificationIfOperStatus)}} 
                                            className='bg-gray-500 hidden'
                                            type="checkbox"
                                            disabled={!canEdit} 
                                        />
                                        <label 
                                            htmlFor="notification-ifOperStatus" 
                                            className={`absolute ${!canEdit && !notificationIfOperStatus ? "bg-blue-950 cursor-not-allowed": ""} ${!canEdit && notificationIfOperStatus ? "bg-green-800 before:translate-x-[16px] cursor-not-allowed": ""} ${canEdit && notificationIfOperStatus ? "bg-green-500 before:translate-x-[16px] cursor-pointer" : ""} ${canEdit && !notificationIfOperStatus ? "bg-blue-800": ""} top-[0] left-[0] w-[40px] h-[24px] rounded-[34px] transition duration-300 before:content-[""] before:absolute before:w-[20px] before:h-[20px] before:rounded-[50%] before:top-[2px] before:left-[2px] drop-shadow-[1px_1px_2px_rgba(0,0,0,0.3)] before:bg-white-50 before:transition before:duration-300`}
                                        />
                                    </div>
                                </div>
                                <div id="info-ifAdminStatus" className="w-full h-fit px-4 flex flex-row items-center justify-between gap-2">
                                    <h4>ifAdminStatus - Estatus Administrativo de la Interfaz</h4>
                                    <div className='relative inline-block w-[40px] h-[24px] m-[10px]'>
                                        <input 
                                            id='notification-ifAdminStatus' 
                                            onClick={() => {handlerNotificationIfAdminStatus(!notificationIfAdminStatus)}} 
                                            className='bg-gray-500 hidden'
                                            type="checkbox"
                                            disabled={!canEdit} 
                                        />
                                        <label 
                                            htmlFor="notification-ifAdminStatus" 
                                            className={`absolute ${!canEdit && !notificationIfAdminStatus ? "bg-blue-950 cursor-not-allowed": ""} ${!canEdit && notificationIfAdminStatus ? "bg-green-800 before:translate-x-[16px] cursor-not-allowed": ""} ${canEdit && notificationIfAdminStatus ? "bg-green-500 before:translate-x-[16px] cursor-pointer" : ""} ${canEdit && !notificationIfAdminStatus ? "bg-blue-800": ""} top-[0] left-[0] w-[40px] h-[24px] rounded-[34px] transition duration-300 before:content-[""] before:absolute before:w-[20px] before:h-[20px] before:rounded-[50%] before:top-[2px] before:left-[2px] drop-shadow-[1px_1px_2px_rgba(0,0,0,0.3)] before:bg-white-50 before:transition before:duration-300`}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>        
                </div>
            }
        </main>
    );
}