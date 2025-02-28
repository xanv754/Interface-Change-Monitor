'use client';

import Navbar from '@components/navbar/navbar';
import InterfaceAssignedCard from '@app/components/cards/assigned';
import FilterForm from '@app/components/forms/filter';
import AlertModal from '@app/components/modals/alert';
import LoadingModal from '@app/components/modals/loading';
import SelectorStatusAssignmentForm from '@/app/components/forms/selectStatusAssignment';
import { CurrentSession } from '@libs/session';
import { AssignmentService } from '@/services/assignment';
import { AssignmentInfoResponseSchema } from '@schemas/assignment';
import { UserShortInfoResponseSchema } from "@schemas/user";
import { Routes } from '@/libs/routes';
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

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
    const pathname = usePathname();
    const router = useRouter();

    const [loading, setLoading] = useState<boolean>(true);
    const [errorInfo, setErrorInfo] = useState<boolean>(false);
    const [errorUpdateStatus, setErrorUpdateStatus] = useState<boolean>(false);
    const [successUpdateStatus, setSuccessUpdateStatus] = useState<boolean>(false);

    const [statusAssignment, setStatusAssignment] = useState<string | null>(null);
    const [filterContent, setFilterContent] = useState<string | null>(null);
    
    const [user, setUser] = useState<UserShortInfoResponseSchema | null>(null);
    const [allAssigned, setAllAssigned] = useState<AssignmentInfoResponseSchema[]>([]);
    const [assignedCheck, setAssignedCheck] = useState<AssignmentInfoResponseSchema[]>([]);
    const [assignedFilter, setAssignedFilter] = useState<AssignmentInfoResponseSchema[]>([]);

    const addChangeCheck = (change: AssignmentInfoResponseSchema) => {
        setAssignedCheck([...assignedCheck, change]);
    }

    const removeChangeCheck = (change: AssignmentInfoResponseSchema) => {
        setAssignedCheck(assignedCheck.filter(c => (c.ip !== change.ip && c.community !== change.community && c.sysname !== change.sysname && c.ifIndex !== change.ifIndex)));
    }

    const filterChange = () => {
        if (filterContent && allAssigned) setAssignedFilter(filterChangeSchemas(allAssigned, filterContent));
    }

    const handlerModalLoaded = () => {
        setTimeout(() => {
            setLoading(false);
        }, 2000);

    }

    const handlerModalErrorInfo = () => {
        setErrorInfo(false);
    }

    const handlerModalErrorUpdateStatus = () => {
        setErrorUpdateStatus(false);
    }

    const handlerModalSuccessUpdateStatus = () => {
        setSuccessUpdateStatus(false);
        router.refresh();
    }

    const handlerChangesCheck = (change: AssignmentInfoResponseSchema, status: boolean) => {
        if (status) {
            addChangeCheck(change);
        } else {
            removeChangeCheck(change);
        }
    }

    const handlerStatus = (status: string | null) => {
        setStatusAssignment(status);
    }

    const handlerFilter = (filter: string | null) => {
        setFilterContent(filter);
    }

    const handlerUpdateStatus = () => {
        if ((statusAssignment) && (assignedCheck.length > 0)) {
            console.log(statusAssignment);
            console.log(assignedCheck);
        }
    }

    const getAssignments = async (token: string) => {
        const data = await AssignmentService.getPendings(token);
        setAllAssigned(data);
    }

    const getData = async () => {
        let currentUser = CurrentSession.getInfoUser();
        let token = CurrentSession.getToken();
        if (currentUser && token) {
            setUser(currentUser);
            await getAssignments(token);
            handlerModalLoaded();
        }
        else {
            handlerModalLoaded();
            setErrorInfo(true);
        }
    };

    useEffect(() => {
        if (filterContent && filterContent.length > 0) {
            filterChange();
        }
        else setAssignedFilter(allAssigned);
    }, [filterContent]);

    useEffect(() => {
        setAssignedFilter(allAssigned);
    }, [allAssigned]);
    
    useEffect(() => {
        getData();
    }, []);

    return (
        <main className="min-w-fit w-full h-screen flex flex-col">
            <LoadingModal showModal={loading} />
            {errorInfo && <AlertModal showModal={true} title='Error al obtener información' message='Ocurrió un error al intentar obtener los cambios recientes. Por favor, inténtelo de nuevo más tarde.' afterAction={handlerModalErrorInfo} />}
            {errorUpdateStatus && <AlertModal showModal={true} title='Error al actualizar el estatus' message='Ocurrió un error al intentar actualizar el estatus de la asignación. Por favor, inténtelo de nuevo más tarde.' afterAction={handlerModalErrorUpdateStatus} />}
            {successUpdateStatus && <AlertModal showModal={true} title='Estatus actualizado' message='El estatus de la asignación ha sido actualizado con éxito.' afterAction={handlerModalSuccessUpdateStatus} />}
            <section className='w-full h-fit px-4 py-1 mb-4 flex flex-col gap-4'>
                <Navbar />
                {user && 
                    <h1 className='text-4xl text-white-50 font-bold px-2 md:px-8'>¡Bienvenido, <span className='italic'>{user.name} {user.lastname}!</span></h1>
                }
                {pathname === Routes.homeAssigned &&
                    <div className='w-full flex flex-col items-center'>
                        <div className='w-fit'>
                            <h2 className='text-center text-3xl text-white-50 font-bold px-4'>Asignaciones</h2>
                            <div className='w-full h-1 mt-1 bg-yellow-500 rounded-full'></div>
                        </div>
                    </div>
                }
            </section>
            <section className='w-full h-full bg-white-100 flex flex-col'>
                <div className={`w-full h-fit bg-gray-950 py-3 mb-4 flex flex-col items-center justify-center gap-2`}>
                    <h3 className='text-xl text-center text-yellow-500 font-bold'>Total de Interfaces Asignadas: <span className={`${(allAssigned.length > 0) ? "text-green-500": "text-gray-400"}`}>{allAssigned.length}</span></h3>
                    <h3 className='text-xl text-center   text-white-55 font-bold'>Seleccione las asignaciones para cambiar su estatus</h3>
                    <div className='w-full h-fit flex flex-row items-center justify-center gap-2'>
                        <SelectorStatusAssignmentForm id='StatusAssignment' label='Estatus de Asignaciones' getValue={handlerStatus} />
                        <button 
                            onClick={handlerUpdateStatus}
                            className={`h-fit px-4 py-1 ${(assignedCheck.length > 0 && statusAssignment) ? "bg-blue-800": "bg-gray-400"} rounded-full text-white-50 transition-all duration-300 ease-in-out ${(assignedCheck.length > 0 && statusAssignment) ? "hover:bg-green-800": "hover:bg-gray-400"}`}>
                                Asignar Estatus
                        </button>
                    </div>
                    <FilterForm getValue={handlerFilter}/>
                </div>
                {user && 
                    <div className={`w-full px-2 ${(assignedFilter && assignedFilter.length > 0) ? "h-fit" : "h-full flex flex-row items-center justify-center"}`}>
                        {assignedFilter && assignedFilter.length > 0 &&
                            assignedFilter.map((change, index) => {
                                return <InterfaceAssignedCard key={index} data={change} handlerData={handlerChangesCheck} />
                            })
                        }
                        {(!assignedFilter || assignedFilter.length <= 0) &&
                            <h2 className='text-center text-2xl text-gray-400 font-bold py-4'>No hay asignaciones</h2>
                        }
                    </div>
                }
                {!user &&
                    <div className={`w-full px-2 h-full flex flex-row items-center justify-center`}>
                        <h2 className='text-center text-2xl text-gray-400 font-bold py-4'>Error al obtener información</h2>
                    </div>
                }
            </section>
        </main>
    );
}