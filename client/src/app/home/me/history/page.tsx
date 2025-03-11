'use client';


import Navbar from '@components/navbar/navbar';
import LoadingModal from '@/app/components/modals/loading';
import AlertModal from '@/app/components/modals/alert';
import PageTitles from '@/app/components/titles/titlePage';
import HistoryInterfaceAssignedCard from '@/app/components/cards/historyAssigned';
import SelectorStatusAssignmentForm from '@/app/components/forms/selectStatusAssignment';
import { CurrentSession } from '@/libs/session';
import { ExcelHandler } from '@libs/excel';
import { AssignmentService } from '@/services/assignment';
import { AssignmentInfoResponseSchema, AssignmentUpdateStatusRequestSchema } from '@/schemas/assignment';
import { useEffect, useState } from "react";
import { UserShortInfoResponseSchema } from '@/schemas/user';

export default function HistoryPersonalView() {
    const [loading, setLoading] = useState<boolean>(true);
    const [errorFile, setErrorFile] = useState<boolean>(false);
    const [errorInfo, setErrorInfo] = useState<boolean>(false);
    const [errorUpdate, setErrorUpdate] = useState<boolean>(false);
    const [successUpdate, setSuccessUpdate] = useState<boolean>(false);

    const [user, setUser] = useState<UserShortInfoResponseSchema | null>(null);
    const [token, setToken] = useState<string | null>(null);

    const [assignmentsSelected, setAssignmentsSelected] = useState<AssignmentInfoResponseSchema[]>([]);
    const [allAssignmentsRevised, setAllAssignmentsRevised] = useState<AssignmentInfoResponseSchema[]>([]);
    const [statusAssignment, setStatusAssignment] = useState<string | null>(null);

    /**
     * Get the information of the user logged in.
     */
    const getData = async () => {
        let currentUser = CurrentSession.getInfoUser();
        let currentToken = CurrentSession.getToken();
        if (currentUser && currentToken) {
            setToken(currentToken);
            setUser(currentUser);
            const data = await AssignmentService.getReviseds(currentToken);
            handlerLoading(false);
            if (data && data.length > 0) setAllAssignmentsRevised(data);
        }
        else {
            handlerLoading(false);
            handlerErrorInfo(true);
        }
    };

    /**
     * Add an assignment selected to the list of interfaces selected.
     * 
     * @param {AssignmentInfoResponseSchema} assignmentSelected Assignment selected.
     */
    const addAssigmentSelected = (assignmentSelected: AssignmentInfoResponseSchema) => {
        setAssignmentsSelected([...assignmentsSelected, assignmentSelected]);
    }

    /**
     * Remove an assignment selected from the list of assignment selected.
     * 
     * @param {AssignmentInfoResponseSchema} AssignmentSelected Assignment selected.
     */
    const removeAssignmentSelected = (AssignmentSelected: AssignmentInfoResponseSchema) => {
        setAssignmentsSelected(assignmentsSelected.filter(c => (
                c.ip !== AssignmentSelected.ip && 
                c.community !== AssignmentSelected.community && 
                c.sysname !== AssignmentSelected.sysname && 
                c.ifIndex !== AssignmentSelected.ifIndex
            ))
        );
    }

    /**
     * Update the status of all the interfaces selected.
     */
    const updateStatus = async () => {
        handlerLoading(true);
        if (token && statusAssignment && assignmentsSelected.length > 0) {
            const data: AssignmentUpdateStatusRequestSchema[] = [];
            assignmentsSelected.map((assigment: AssignmentInfoResponseSchema) => {
                data.push({
                    idAssignment: assigment.idAssignment,
                    newStatus: statusAssignment
                });
            });
            if (data.length > 0) {
                const status = await AssignmentService.updateStatusAssignments(token, data)
                if (status) {
                    handlerLoading(false);
                    handlerSuccessUpdate(true);
                }
                else {
                    handlerLoading(false);
                    handlerErrorUpdate(true);
                }
            } else {
                handlerLoading(false);
                handlerErrorInfo(false);
            }
        } else {
            handlerLoading(false);
            handlerErrorInfo(false);
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
     * Handler for success update status of assignments.
     * 
     * @param isSuccess 
     */
    const handlerSuccessUpdate = (isSuccess: boolean = false) => {
        setSuccessUpdate(isSuccess);
    }

    /**
     * Handler to add or remove an assignment from the list of assignments selected.
     * 
     * @param {AssignmentInfoResponseSchema} assignment Assignment selected.
     * @param {boolean} selected If the assignment is selected or not.
     */
    const handlerAssignmentSelected = (assignment: AssignmentInfoResponseSchema, selected: boolean) => {
        if (selected) addAssigmentSelected(assignment);
        else removeAssignmentSelected(assignment);
    }

    /**
     * Handler for user error update status.
     * 
     * @param {boolean} isThereAnError If there is an error or not.
     */
    const handlerErrorUpdate = (isThereAnError: boolean = false) => {
        setErrorUpdate(isThereAnError);
    }

    /**
     * Handler for history file error.
     * 
     * @param {boolean} isThereAnError If there is an error or not.
     */
    const handlerErrorFile = (isThereAnError: boolean = false) => {
        setErrorFile(isThereAnError);
    }

    /**
     * Handler to get the status of the assignment that will be assigned to the interfaces selected.
     * 
     * @param {string | null} status The status of the assignment.
     */
    const handlerStatusAssignment = (status: string | null) => {
        setStatusAssignment(status);
    }

    const handlerDownloadHistory = () => {
        if (user && allAssignmentsRevised.length > 0) {
            let status = ExcelHandler.getHistoryOfUser(user.name, allAssignmentsRevised);
            if (!status) handlerErrorFile(true);
        } else if (user && allAssignmentsRevised.length <= 0) return;
        else handlerErrorFile(true);
    }

    useEffect(() => {
        getData();
    }, []);

    return (
        <main className="min-w-fit w-full h-screen flex flex-col">
            <LoadingModal showModal={loading} />
            {errorInfo && 
                <AlertModal 
                    showModal={true} 
                    title='Error al obtener información' 
                    message='Ocurrió un error al intentar obtener los cambios recientes. Por favor, refresca la página e inténtelo de nuevo. Si el error persiste, consulte a soporte.' 
                    afterAction={handlerErrorInfo} 
                />
            }
            {errorFile && 
                <AlertModal 
                    showModal={true} 
                    title='Error al generar el archivo'
                    message='Ocurrió un error al intentar generar el historial para descargar. Por favor, refresca la página e inténtelo de nuevo. Si el error persiste, consulte a soporte.' 
                    afterAction={handlerErrorFile} 
                />
            }
            {errorUpdate && 
                <AlertModal 
                    showModal={true} 
                    title='Error al actualizar el estatus de las asignaciones' 
                    message='Ocurrió un error al intentar actualizar el estatus de la asignación. Por favor, refresca la página e inténtelo de nuevo. Si el error persiste, consulte a soporte.' 
                    afterAction={handlerErrorUpdate} 
                />
            }
            {successUpdate && 
                <AlertModal 
                    showModal={true} 
                    title='Estatus actualizado' 
                    message='El estatus de la asignación ha sido actualizado con éxito. Refresca la página para ver los cambios.'
                    afterAction={handlerSuccessUpdate} 
                />
            }
            <section id='header' className='w-full h-fit px-4 py-1 mb-4 flex flex-col gap-4'>
                <Navbar />
                <PageTitles />
            </section>
            <section id='content' className={`w-full ${allAssignmentsRevised.length > 0 ? 'min-h-fit h-full' : 'h-full'} bg-white-100 flex flex-col`}>
                <div id='content-header' className='w-full h-fit bg-gray-950 py-3 mb-4 flex flex-col items-center justify-center gap-2'>
                    <h3 id='label-history-download' className='text-xl text-white-55 font-bold'>Descargar mi historial</h3>
                    <button 
                        id='download-history'
                        onClick={handlerDownloadHistory}
                        className={`px-4 py-1 ${(allAssignmentsRevised.length > 0) ? "bg-blue-800": "bg-gray-400"} rounded-full text-white-50 transition-all duration-300 ease-in-out ${(allAssignmentsRevised.length > 0) ? "hover:bg-green-800": "hover:bg-gray-400"}`}>
                        Descargar
                    </button>
                    <h3 id='label-change-status-assignment' className='text-xl text-white-55 font-bold'>Cambiar estatus de asignaciones revisadas</h3>
                    <SelectorStatusAssignmentForm id='status-selector' label='Estatus de Asignaciones' getValue={handlerStatusAssignment} />
                    <button 
                        id='update-status'
                        onClick={updateStatus}
                        className={`h-fit px-4 py-1 ${(assignmentsSelected.length > 0 && statusAssignment) ? "bg-blue-800": "bg-gray-400"} rounded-full text-white-50 transition-all duration-300 ease-in-out ${(assignmentsSelected.length > 0 && statusAssignment) ? "hover:bg-green-800": "hover:bg-gray-400"}`}>
                            Asignar Estatus
                    </button>
                </div>
                {user &&
                    <div id='interfaces-revised' className={`w-full px-2 ${(allAssignmentsRevised.length > 0) ? "h-fit" : "h-full flex flex-row items-center justify-center"}`}>
                        {allAssignmentsRevised.length > 0 &&
                            allAssignmentsRevised.map((change, index) => {
                                return <HistoryInterfaceAssignedCard key={index} data={change} handlerData={handlerAssignmentSelected} />
                            })
                        }
                        {(allAssignmentsRevised.length <= 0) &&
                            <h2 className='text-center text-2xl text-gray-400 font-bold py-4'>Historial Vacío</h2>
                        }
                    </div>
                }
                {!user &&
                    <div id='content-error' className={`w-full px-2 h-full flex flex-row items-center justify-center`}>
                        <h2 id='content-message-error' className='text-center text-2xl text-gray-400 font-bold py-4'>Error al obtener información de usuario</h2>
                    </div>
                }
            </section>
        </main>
    );
}