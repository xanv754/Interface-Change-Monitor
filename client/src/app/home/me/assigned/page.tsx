'use client';

import Navbar from '@components/navbar/navbar';
import WelcomeTitle from '@app/components/titles/welcome';
import PageTitles from '@app/components/titles/titlePage';
import InterfaceAssignedCard from '@app/components/cards/assigned';
import FilterForm from '@app/components/forms/filter';
import AlertModal from '@app/components/modals/alert';
import LoadingModal from '@app/components/modals/loading';
import SelectorStatusAssignmentForm from '@/app/components/forms/selectStatusAssignment';
import { CurrentSession } from '@libs/session';
import { AssignmentService } from '@/services/assignment';
import { AssignmentInfoResponseSchema, AssignmentUpdateStatusRequestSchema } from '@schemas/assignment';
import { UserShortInfoResponseSchema } from "@schemas/user";
import { useEffect, useState } from "react";

/**
 * Search an word in each field of the interfaces with changes detected.
 * 
 * @param {AssignmentInfoResponseSchema[]} changes List of interfaces detected.
 * @param {string} searchString Word to search.
 * @returns {AssignmentInfoResponseSchema[]} List of interfaces with the word included in some field.
 */
function filterChangeSchemas(changes: AssignmentInfoResponseSchema[], searchString: string): AssignmentInfoResponseSchema[] {
    const lowerCaseSearchString = searchString.toLowerCase();
    return changes.filter(change => {
        const matchesChangeSchema = Object.values(change).some(value => {
            if (typeof value === 'string') {
                return value.toLowerCase().includes(lowerCaseSearchString);
            } else if (typeof value === 'number') {
                return value.toString().includes(lowerCaseSearchString);
            }
            return false;
        });
        return matchesChangeSchema;
    });
}

export default function AssignedView() {
    const [loading, setLoading] = useState<boolean>(true);
    const [errorInfo, setErrorInfo] = useState<boolean>(false);
    const [errorUpdate, setErrorUpdate] = useState<boolean>(false);
    const [successUpdate, setSuccessUpdate] = useState<boolean>(false);

    const [statusAssignment, setStatusAssignment] = useState<string | null>(null);
    const [filterContent, setFilterContent] = useState<string | null>(null);
    
    const [user, setUser] = useState<UserShortInfoResponseSchema | null>(null);
    const [token, setToken] = useState<string | null>(null);

    const [selectAllAssignment, setSelectAllAssignment] = useState<boolean>(false);
    const [allAssignments, setAllAssignments] = useState<AssignmentInfoResponseSchema[]>([]);
    const [assignmentsSelected, setAssignmentsSelected] = useState<AssignmentInfoResponseSchema[]>([]);
    const [assignmentsDisplay, setAssignmentsDisplay] = useState<AssignmentInfoResponseSchema[]>([]);

    /**
     * Get the information of the user logged in and your pending assignments.
     */
    const getData = async () => {
        let currentUser = CurrentSession.getInfoUser();
        let currentToken = CurrentSession.getToken();
        if (currentUser && currentToken) {
            setToken(currentToken);
            setUser(currentUser);
            const data = await AssignmentService.getPendings(currentToken);
            if (data && data.length > 0) setAllAssignments(data);
            handlerLoading(false);
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
            c.ifIndex !== AssignmentSelected.ifIndex))
        );
    }

    /**
     * Remove assignments that have been updated.
     * 
     * @param {AssignmentUpdateStatusRequestSchema[]} assignmentsUpdated Assignments updated.
     */
    const removeAssignments = (assignmentsUpdated: AssignmentUpdateStatusRequestSchema[]) => {
        setAllAssignments(allAssignments.filter(c => (
                !assignmentsUpdated.map(a => a.idAssignment).includes(c.idAssignment)
            ))
        );
    }

    /**
     * Filter the list of interfaces assigned by an content.
     * That list of interfaces will be displayed in the page.
     */
    const filterAssignmentsDisplay = () => {
        if (filterContent && allAssignments) setAssignmentsDisplay(filterChangeSchemas(allAssignments, filterContent));
    }

    /**
     * Update the status of all the interfaces selected.
     */
    const UpdateStatus = async () => {
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
                    removeAssignments(data);
                    handlerLoading(false);
                    handlerSuccessUpdate(true);
                }
                else {
                    handlerLoading(false);
                    handlerErrorUpdate(true);
                }
            } else {
                handlerLoading(false);
                handlerErrorInfo(true);    
            }
        } else {
            handlerLoading(false);
            handlerErrorInfo(true);
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
     * Handler for user error update status.
     * 
     * @param {boolean} isThereAnError If there is an error or not.
     */
    const handlerErrorUpdate = (isThereAnError: boolean = false) => {
        setErrorUpdate(isThereAnError);
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
     * Handler to select all assignments.
     * 
     * @param {boolean} isChecked If all the assignments are selected or not.
     */
    const handlerSelectAllAssignment = (isChecked: boolean = false) => {
        setSelectAllAssignment(isChecked);
    }

    /**
     * Handler to get the status of the assignment that will be assigned to the interfaces selected.
     * 
     * @param {string | null} status The status of the assignment.
     */
    const handlerStatusAssignment = (status: string | null) => {
        setStatusAssignment(status);
    }

    /**
     * Handler to get the words to filter the interfaces with changes detected.
     * 
     * @param {string | null} filter Words to filter the interfaces.
     */
    const handlerFilterContent = (filter: string | null) => {
        setFilterContent(filter);
    }

    useEffect(() => {
        if (filterContent && filterContent.length > 0) filterAssignmentsDisplay();
        else setAssignmentsDisplay(allAssignments);
    }, [filterContent]);

    useEffect(() => {
        setAssignmentsDisplay(allAssignments);
    }, [allAssignments]);
    
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
                    message='Ocurrió un error al intentar obtener la información. Por favor, refresca la página e inténtelo de nuevo. Si el error persiste, consulte a soporte.' 
                    afterAction={handlerErrorInfo} 
                />
            }
            {errorUpdate && 
                <AlertModal 
                    showModal={true} 
                    title='Error al actualizar el estatus' 
                    message='Ocurrió un error al intentar actualizar el estatus de la asignación. Por favor, refresca la página e inténtelo de nuevo. Si el error persiste, consulte a soporte.' 
                    afterAction={handlerErrorUpdate} 
                />
            }
            {successUpdate && 
                <AlertModal 
                    showModal={true} 
                    title='Estatus actualizado' 
                    message='El estatus de la asignación ha sido actualizado con éxito.' 
                    afterAction={handlerSuccessUpdate} 
                />
            }
            <section id='header' className='w-full h-fit px-4 py-1 mb-4 flex flex-col gap-4'>
                <Navbar />
                <WelcomeTitle user={user} />
                <PageTitles />
            </section>
            <section id='content' className={`w-full ${allAssignments.length > 0 ? 'min-h-fit h-full' : 'h-full'} bg-white-100 flex flex-col`}>
                <div id='content-header' className='w-full h-fit bg-gray-950 py-3 mb-4 flex flex-col items-center justify-center gap-2'>
                    <h3 id='total-interfaces' className='text-xl text-center text-yellow-500 font-bold'>Total de Interfaces Asignadas: <span className={`${(allAssignments.length > 0) ? "text-green-500": "text-gray-400"}`}>{allAssignments.length}</span></h3>
                    <h3 id='label-change-status-assignment' className='text-xl text-center text-white-55 font-bold'>Seleccione las asignaciones para cambiar su estatus</h3>
                    <div id='change-status-assignment' className='w-full h-fit flex flex-row items-center justify-center gap-2'>
                        <SelectorStatusAssignmentForm id='status-selector' label='Estatus de Asignaciones' getValue={handlerStatusAssignment} pendingDisabled={true} />
                        <button 
                            id='update-status'
                            onClick={UpdateStatus}
                            className={`h-fit px-4 py-1 ${(assignmentsSelected.length > 0 && statusAssignment) ? "bg-blue-800": "bg-gray-400"} rounded-full text-white-50 transition-all duration-300 ease-in-out ${(assignmentsSelected.length > 0 && statusAssignment) ? "hover:bg-green-800": "hover:bg-gray-400"}`}>
                                Asignar Estatus
                        </button>
                    </div>
                    <FilterForm id='filter-interfaces' getValue={handlerFilterContent}/>
                </div>
                {user && 
                    <div id='interfaces-assigned' className={`w-full px-2 ${(assignmentsDisplay && assignmentsDisplay.length > 0) ? "h-fit" : "h-full flex flex-row items-center justify-center"}`}>
                        {assignmentsDisplay.length > 0 &&
                            <button
                                id='all-select'
                                onClick={() => {handlerSelectAllAssignment(!selectAllAssignment)}}
                                className={`px-4 py-1 mb-2 bg-blue-800 rounded-full text-white-50 transition-all duration-300 ease-in-out ${(assignmentsDisplay.length > 0 && !selectAllAssignment) ? "hover:bg-green-800": "hover:bg-red-800"}`}
                            >
                                {!selectAllAssignment && "Seleccionar todos"}
                                {selectAllAssignment && "Deseleccionar todos"}
                            </button>
                        }
                        {assignmentsDisplay.length > 0 &&
                            assignmentsDisplay.map((change, index) => {
                                return <InterfaceAssignedCard key={index} data={change} handlerData={handlerAssignmentSelected} selectAllChecked={selectAllAssignment} />
                            })
                        }
                        {assignmentsDisplay.length <= 0 &&
                            <h2 className='text-center text-2xl text-gray-400 font-bold py-4'>No hay asignaciones</h2>
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