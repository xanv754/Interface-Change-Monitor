'use client';

import Navbar from '@components/navbar/navbar';
import WelcomeTitle from '@/app/components/titles/welcome';
import PageTitles from '@app/components/titles/titlePage';
import AlertModal from '@app/components/modals/alert';
import LoadingModal from '@/app/components/modals/loading';
import InterfaceAssignCard from '@app/components/cards/assign';
import FilterForm from '@app/components/forms/filter';
import SelectorOperatorForm from '@app/components/forms/selectOperator';
import { CurrentSession } from '@libs/session';
import { AdministrationService } from '@/services/administration';
import { AssignmentService } from '@/services/assignment';
import { ChangeResponseSchema } from '@schemas/changes';
import { AssignRequestSchema } from '@schemas/assignment';
import { UserShortInfoResponseSchema, UserResponseSchema } from "@schemas/user";
import { useEffect, useState } from "react";

/**
 * Filter list of interface changes by an word.
 * 
 * @param {ChangeResponseSchema[]} changes List of interface changes.
 * @param {string} searchString Word to filter the interface changes.
 * @returns {ChangeResponseSchema[]} List with all interfaces that match the word.
 */
function filterChangeByString(changes: ChangeResponseSchema[], searchString: string): ChangeResponseSchema[] {
    const lowerCaseSearchString = searchString.toLowerCase();

    return changes.filter(change => {
        const matchesChangeSchema = Object.values(change).some(value => {
            if (typeof value === 'string') {
                return value.toLowerCase().includes(lowerCaseSearchString);
            }
            return false;
        });
        const matchesOldInterface = Object.values(change.oldInterface).some(value => {
            if (typeof value === 'string') {
                return value.toLowerCase().includes(lowerCaseSearchString);
            }
            return false;
        });
        const matchesNewInterface = Object.values(change.newInterface).some(value => {
            if (typeof value === 'string') {
                return value.toLowerCase().includes(lowerCaseSearchString);
            }
            return false;
        });

        return matchesChangeSchema || matchesOldInterface || matchesNewInterface;
    });
}

/**
 * Find a user in a list of users.
 * 
 * @param {UserResponseSchema[]} users List of users.
 * @param {string} username Username to filter the users.
 * @returns {UserResponseSchema | null} User that match the username.
 */
function findUser(users: UserResponseSchema[], username: string): UserResponseSchema | null {
    return users.find(user => user.username === username) || null;
}

export default function AssignView() {
    const [loading, setLoading] = useState<boolean>(true);
    const [errorInfo, setErrorInfo] = useState<boolean>(false);
    const [errorAssign, setErrorAssign] = useState<boolean>(false);
    const [successAssign, setSuccessAssign] = useState<boolean>(false);

    const [token, setToken] = useState<string | null>(null);
    const [user, setUser] = useState<UserShortInfoResponseSchema | null>(null);
    const [allUsers, setAllUsers] = useState<UserResponseSchema[]>([]);
    const [allChanges, setAllChanges] = useState<ChangeResponseSchema[]>([]);

    const [filterContent, setFilterContent] = useState<string | null>(null);
    
    const [userSelect, setUserSelect] = useState<UserResponseSchema | null>(null);
    const [selectAllChanges, setSelectAllChanges] = useState<boolean>(false);
    const [changesCheck, setChangesCheck] = useState<ChangeResponseSchema[]>([]);
    const [changesFilter, setChangesFilter] = useState<ChangeResponseSchema[]>([]);

    /**
     * Get the information of the user logged in, all the changes detected on the day and all the users.
     */
    const getData = async () => {
        let currentToken = CurrentSession.getToken();
        let currentUser = CurrentSession.getInfoUser();
        if (currentToken && currentUser) {
            setToken(currentToken)
            setUser(currentUser);
            await getAssignments(currentToken);
            await getUsers(currentToken);
            handlerLoading(false);
        }
        else {
            handlerLoading(false);
            setErrorInfo(true);
        }
    };

    /**
     * Get all interfaces changes detected on the day.
     * 
     * @param {string} token Token of the user logged in.
     */
    const getAssignments = async (token: string) => {
        const data = await AdministrationService.getChanges(token);
        setAllChanges(data);
    }

    /**
     * Get all users of the system.
     * 
     * @param {string} token Token of the user logged in.
     */
    const getUsers = async (token: string) => {
        const data = await AdministrationService.getAllUsers(token);
        setAllUsers(data);
    }

    /**
     * Add an interface to the list of changes selected (checked).
     * 
     * @param {ChangeResponseSchema} change Interface to add to the list of changes selected (checked).
     */
    const addChangeCheck = (change: ChangeResponseSchema) => {
        setChangesCheck([...changesCheck, change]);
    }

    /**
     * Remove an interface from the list of changes selected (checked).
     * 
     * @param {ChangeResponseSchema} change Interface to remove from the list of changes selected (checked).
     */
    const removeChangeCheck = (change: ChangeResponseSchema) => {
        setChangesCheck(changesCheck.filter(c => (c.ip !== change.ip && c.community !== change.community && c.sysname !== change.sysname && c.ifIndex !== change.ifIndex)));
    }

    /**
     * Discard of list of changes assigned of the list of changes to be assigned.
     * 
     * @param {ChangeResponseSchema[]} changesAssigned List of interfaces changes assigned.
     */
    const discardAssignmentsAssigned = (changesAssigned: ChangeResponseSchema[]) => {
        setAllChanges(allChanges.filter(c => (changesAssigned.map(ca => ca.ip + ca.community + ca.sysname + ca.ifIndex).indexOf(c.ip + c.community + c.sysname + c.ifIndex) === -1)));
    }

    /**
     * Automatically assign all the changes selected (checked).
     */
    const autoAllAssign = () => {
        console.log("Asignando automáticamente...");
    }

    /**
     * Assign all the changes selected (checked) to the user selected.
     */
    const newAssign = async () => {
        handlerLoading(true);
        if (user && token && userSelect && changesCheck.length > 0) {
            let data: AssignRequestSchema[] = [];
            changesCheck.map(change => {
                data.push({
                    newInterface: change.newInterface.id,
                    oldInterface: change.oldInterface.id,
                    operator: userSelect.username,
                    assignedBy: `${user.name} ${user.lastname}`,
                })
            });
            let status = await AssignmentService.addAssignment(token, data);
            if (status) {
                handlerLoading(false);
                setSuccessAssign(true);
                discardAssignmentsAssigned(changesCheck);
            }
            else {
                handlerLoading(false);
                setErrorAssign(true);
            }
        } else {
            handlerLoading(false);
            setErrorAssign(true);
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
        setErrorAssign(isThereAnError);
    }

    /**
     * Handler for success update status of assignments.
     * 
     * @param isSuccess 
     */
    const handlerSuccessUpdate = (isSuccess: boolean = false) => {
        setSuccessAssign(isSuccess);
    }

    /**
     * Handler to filter the list of changes that displayed.
     */
    const handlerFilterChange = () => {
        if (filterContent && allChanges) setChangesFilter(filterChangeByString(allChanges, filterContent));
    }

    /**
     * Handler to get the content to filter the list of changes that displayed.
     * 
     * @param {string | null} filter Word to filter.
     */
    const handlerFilter = (filter: string | null) => {
        setFilterContent(filter);
    }

    /**
     * Handler to add or remove of an change from the list of changes selected (checked).
     * 
     * @param {ChangeResponseSchema} change Interface change selected (checked).
     * @param {boolean} status Status of selection. If true, the interface change has been selected.
     */
    const handlerChangesCheck = (change: ChangeResponseSchema, status: boolean) => {
        if (status) addChangeCheck(change);
        else removeChangeCheck(change);
    }

    /**
     * Handler to get the user to assign to the changes selected (checked).
     * 
     * @param {string | null} username Username to select.
     */
    const handlerSelectUser = (username: string | null) => {
        if (username) {
            const user = findUser(allUsers, username);
            if (user) setUserSelect(user);
            else setUserSelect(null);
        } else setUserSelect(null);
    }

    /**
     * Handler to select all the changes detected.
     * 
     * @param {boolean} isChecked If all the changes are selected or not.
     */
    const handlerSelectAllChanges = (isChecked: boolean = false) => {
        setSelectAllChanges(isChecked);
    }
    
    useEffect(() => {
        if (filterContent && filterContent.length > 0) handlerFilterChange();
        else setChangesFilter(allChanges);
    }, [filterContent]);

    useEffect(() => {
        setChangesFilter(allChanges);
    }, [allChanges]);
    
    useEffect(() => {
        getData();
    }, []);

    return (
        <main className="w-full h-screen flex flex-col">
            <LoadingModal showModal={loading} />
            {errorInfo && 
                <AlertModal 
                    showModal={true} 
                    title='Error al obtener información' 
                    message='Ocurrió un error al intentar obtener los cambios recientes. Por favor, refresca la página e inténtelo de nuevo. Si el error persiste, consulte a soporte.' 
                    afterAction={handlerErrorInfo}
                />
            }
            {errorAssign && 
                <AlertModal 
                    showModal={true} 
                    title='Error al asignar' 
                    message='Ha fallado la asignación para el usuario seleccionado. Por favor, refresca la página e inténtelo de nuevo. Si el error persiste, consulte a soporte.' 
                    afterAction={handlerErrorUpdate}
                />
            }
            {successAssign && 
                <AlertModal 
                    showModal={true} 
                    title='Asignaciones realizadas' 
                    message='Se han realizado las asignaciones correctamente.'
                    afterAction={handlerSuccessUpdate}
                />
            }
            <section id='header' className='w-full h-fit px-4 py-1 mb-4 flex flex-col gap-4'>
                <Navbar />
                <WelcomeTitle user={user} />
                <PageTitles />
            </section>
            <section id='content' className={`w-full h-full min-h-fit bg-white-100 flex flex-col`}>
                <div id='content-header' className='w-full h-fit bg-gray-950 mb-4 py-3 flex flex-col items-center justify-center gap-2'>
                    <h3 id='total-changes-detected' className='text-xl text-center text-yellow-500 font-bold'>Total de Interfaces con Cambios Encontrados: <span className={`${(allChanges.length > 0) ? "text-green-500": "text-gray-400"}`}>{allChanges.length}</span></h3>
                    <h3 id='label-change-selection' className='text-xl text-center text-white-55 font-bold'>Seleccione las interfaces para asignar a un usuario</h3>
                    <div id='change-selection' className='w-fit h-fit flex flex-row items-center justify-center gap-2'>
                        <SelectorOperatorForm id='user-selector' label='Asignar interfaces a' options={allUsers} getValue={handlerSelectUser} />
                        <button
                            id='manual-assign'
                            onClick={newAssign}
                            className={`h-fit px-4 py-1 ${(changesCheck.length > 0 && userSelect) ? "bg-blue-800": "bg-gray-400"} rounded-full text-white-50 transition-all duration-300 ease-in-out ${(changesCheck.length > 0 && userSelect) ? "hover:bg-green-800": "hover:bg-gray-400 cursor-not-allowed"}`}
                        >
                                Asignar
                        </button>
                    </div>
                    <FilterForm id='filter-interfaces' getValue={handlerFilter}/>
                    <button 
                        id='auto-assign'
                        onClick={autoAllAssign}
                        className={`px-4 py-1 ${(changesCheck.length > 0) ? "bg-blue-800": "bg-gray-400"} rounded-full text-white-50 transition-all duration-300 ease-in-out ${(changesCheck.length > 0) ? "hover:bg-green-800": "hover:bg-gray-400 cursor-not-allowed"}`}
                    >
                            Asignación Automática
                    </button>
                </div>
                <div id='changes-detected' className={`w-full ${(changesFilter.length > 0) ? "h-fit px-2" : "h-full flex flex-row items-center justify-center"}`}>
                    {changesFilter.length > 0 && 
                        <button
                            id='all-select'
                            onClick={() => {handlerSelectAllChanges(!selectAllChanges)}}
                            className={`px-4 py-1 mb-2 bg-blue-800 rounded-full text-white-50 transition-all duration-300 ease-in-out ${(changesFilter.length > 0 && !selectAllChanges) ? "hover:bg-green-800": "hover:bg-red-800"}`}
                        >
                            {!selectAllChanges && "Seleccionar todos"}
                            {selectAllChanges && "Deseleccionar todos"}
                        </button>
                    }
                    {changesFilter.length > 0 &&    
                        changesFilter.map((change: ChangeResponseSchema, index: number) => {
                            return <InterfaceAssignCard key={index} data={change} handlerData={handlerChangesCheck} allChecked={selectAllChanges} />
                        })
                    }
                    {(!changesFilter || changesFilter.length <= 0) &&
                        <h2 id='no-changes' className='text-center text-2xl text-gray-400 font-bold py-4'>No hay cambios</h2>
                    }
                </div>
            </section>
        </main>
    );
}