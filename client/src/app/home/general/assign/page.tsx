'use client';

import Navbar from '@components/navbar/navbar';
import AlertModal from '@/app/components/modals/alert';
import InterfaceAssignCard from '@app/components/cards/assign';
import FilterForm from '@app/components/forms/filter';
import SelectorOperatorForm from '@/app/components/forms/selectOperator';
import { CurrentSession } from '@libs/session';
import { AdministrationService } from '@/services/administration';
import { AssignmentService } from '@/services/assignment';
import { ChangeResponseSchema } from '@schemas/changes';
import { AssignRequestSchema } from '@schemas/assignment';
import { UserShortInfoResponseSchema, UserResponseSchema } from "@schemas/user";
import { Routes } from '@libs/routes';
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

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

function finUser(users: UserResponseSchema[], username: string): UserResponseSchema | null {
    return users.find(user => user.username === username) || null;
}

export default function AssignView() {
    const pathname = usePathname();

    const [errorInfo, setErrorInfo] = useState<boolean>(false);
    const [errorAssign, setErrorAssign] = useState<boolean>(false);
    const [successAssign, setSuccessAssign] = useState<boolean>(false);

    const [token, setToken] = useState<string | null>(null);
    const [user, setUser] = useState<UserShortInfoResponseSchema | null>(null);
    const [allUsers, setAllUsers] = useState<UserResponseSchema[]>([]);
    const [allChanges, setAllChanges] = useState<ChangeResponseSchema[]>([]);

    const [filterContent, setFilterContent] = useState<string | null>(null);
    
    const [userSelect, setUserSelect] = useState<UserResponseSchema | null>(null);

    const [changesCheck, setChangesCheck] = useState<ChangeResponseSchema[]>([]);
    const [changesFilter, setChangesFilter] = useState<ChangeResponseSchema[]>([]);

    const addChangeCheck = (change: ChangeResponseSchema) => {
        setChangesCheck([...changesCheck, change]);
    }

    const removeChangeCheck = (change: ChangeResponseSchema) => {
        setChangesCheck(changesCheck.filter(c => (c.ip !== change.ip && c.community !== change.community && c.sysname !== change.sysname && c.ifIndex !== change.ifIndex)));
    }

    const removeAllChanges = (changeAssigned: ChangeResponseSchema[]) => {
        setAllChanges(allChanges.filter(c => (changeAssigned.map(ca => ca.ip + ca.community + ca.sysname + ca.ifIndex).indexOf(c.ip + c.community + c.sysname + c.ifIndex) === -1)));
    }

    const filterChange = () => {
        if (filterContent && allChanges) setChangesFilter(filterChangeByString(allChanges, filterContent));
    }

    const handlerFilter = (filter: string | null) => {
        setFilterContent(filter);
    }

    const handlerChangesCheck = (change: ChangeResponseSchema, status: boolean) => {
        if (status) {
            addChangeCheck(change);
        } else {
            removeChangeCheck(change);
        }
    }

    const handlerSelectUser = (username: string | null) => {
        if (username) {
            const user = finUser(allUsers, username);
            if (user) setUserSelect(user);
            else setUserSelect(null);
        } else setUserSelect(null);
    }
    
    const newAssign = async () => {
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
                setSuccessAssign(true);
                removeAllChanges(changesCheck);
            }
            else setErrorAssign(true);
        }
    }

    const autoAllAssign = () => {
        console.log("Asignando automáticamente...");
    }

    const getAssignments = async (token: string) => {
        const data = await AdministrationService.getChanges(token);
        setAllChanges(data);
    }

    const getUsers = async (token: string) => {
        const data = await AdministrationService.getAllUsers(token);
        setAllUsers(data);
    }

    const getData = async () => {
        let currentToken = CurrentSession.getToken();
        let currentUser = CurrentSession.getInfoUser();
        if (currentToken && currentUser) {
            setToken(currentToken)
            setUser(currentUser);
            await getAssignments(currentToken);
            await getUsers(currentToken);
        }
        else setErrorInfo(true);
    };

    useEffect(() => {
        if (filterContent && filterContent.length > 0) filterChange();
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
            {errorInfo && <AlertModal showModal={true} title='Error al obtener información' message='Ocurrió un error al intentar obtener los cambios recientes. Por favor, inténtelo de nuevo más tarde.' />}
            {errorAssign && <AlertModal showModal={true} title='Error al asignar' message='Ha fallado la asignación para el usuario seleccionado. Por favor, inténtelo de nuevo más tarde.' />}
            {successAssign && <AlertModal showModal={true} title='Asignaciones realizadas' message='Se han realizado las asignaciones correctamente.' />}
            <section className='w-full h-fit px-4 py-1 mb-4 flex flex-col gap-4'>
                <Navbar />
                {user && 
                    <h1 className='text-4xl text-white-50 font-bold px-2 md:px-8'>¡Bienvenido, <span className='italic'>{user.name} {user.lastname}!</span></h1>
                }
                {pathname === Routes.homeAssign &&
                    <div className='w-full flex flex-col items-center'>
                        <div className='w-fit'>
                            <h2 className='text-center text-3xl text-white-50 font-bold px-4'>Asignaciones</h2>
                            <div className='w-full h-1 mt-1 bg-yellow-500 rounded-full'></div>
                        </div>
                    </div>
                }
            </section>
            <section id='content' className={`w-full h-full min-h-fit bg-white-100 flex flex-col`}>
                <div className='w-full h-fit bg-gray-950 mb-4 py-3 flex flex-col items-center justify-center gap-2'>
                    <h3 className='text-xl text-center text-yellow-500 font-bold'>Total de Interfaces con Cambios Encontrados: <span className={`${(allChanges.length > 0) ? "text-green-500": "text-gray-400"}`}>{allChanges.length}</span></h3>
                    <h3 className='text-xl text-center text-white-55 font-bold'>Seleccione las interfaces para asignar a un usuario</h3>
                    <div className='w-fit h-fit flex flex-row items-center justify-center gap-2'>
                        <SelectorOperatorForm id='StatusAssignment' label='Asignar interfaces a' options={allUsers} getValue={handlerSelectUser} />
                        <button 
                            onClick={newAssign}
                            className={`h-fit px-4 py-1 ${(changesCheck.length > 0 && userSelect) ? "bg-blue-800": "bg-gray-400"} rounded-full text-white-50 transition-all duration-300 ease-in-out ${(changesCheck.length > 0 && userSelect) ? "hover:bg-green-800": "hover:bg-gray-400 cursor-not-allowed"}`}>
                                Asignar
                        </button>
                    </div>
                    <FilterForm getValue={handlerFilter}/>
                    <button 
                        onClick={autoAllAssign}
                        className={`px-4 py-1 ${(allChanges.length > 0) ? "bg-blue-800": "bg-gray-400"} rounded-full text-white-50 transition-all duration-300 ease-in-out ${(allChanges.length > 0) ? "hover:bg-green-800": "hover:bg-gray-400 cursor-not-allowed"}`}>
                            Asignación Automática
                    </button>
                </div>
                <div className={`w-full ${(changesFilter.length > 0) ? "h-fit px-2" : "h-full flex flex-row items-center justify-center"}`}>
                    {changesFilter.length > 0 &&    
                        changesFilter.map((change: ChangeResponseSchema, index: number) => {
                            return <InterfaceAssignCard key={index} data={change} handlerData={handlerChangesCheck} />
                        })
                    }
                    {(!changesFilter || changesFilter.length <= 0) &&
                        <h2 className='text-center text-2xl text-gray-400 font-bold py-4'>No hay cambios</h2>
                    }
                </div>
            </section>
        </main>
    );
}