'use client';

import Navbar from '@components/navbar/navbar';
import InterfaceAssignedCard from '@/app/components/card/assigned';
import FilterForm from '@/app/components/form/filter';
import SelectorForm from '@/app/components/form/select';
import { StatusAssignment } from '@/libs/types';
import { ChangeSchema } from '@/schemas/changes';
import { UserInfoSchema } from "@schemas/user";
import { Routes } from '@/libs/routes';
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

const changesExample: ChangeSchema[] = [
    {
        ip: "192.168.1.1",
        community: "public",
        sysname: "eth0",
        ifIndex: 1,
        oldInterface: {
            id: 1,
            date: "2023-03-01T00:00:00.000Z",
            ifName: "eth0",
            ifDescr: "Ethernet Interface",
            ifAlias: "eth0",
            ifSpeed: 1000,
            ifHighSpeed: 1000,
            ifPhysAddress: "00:00:00:00:00:00",
            ifType: "ether",
            ifOperStatus: "up",
            ifAdminStatus: "up",
            ifPromiscuousMode: false,
            ifConnectorPresent: true,
            ifLastChange: "2023-03-01T00:00:00.000Z",
        },
        newInterface: {
            id: 1,
            date: "2023-03-01T00:00:00.000Z",
            ifName: "eth0",
            ifDescr: "Ethernet Interface",
            ifAlias: "eth0",
            ifSpeed: 1000,
            ifHighSpeed: 1000,
            ifPhysAddress: "00:00:00:00:00:00",
            ifType: "ether",
            ifOperStatus: "up",
            ifAdminStatus: "up",
            ifPromiscuousMode: false,
            ifConnectorPresent: true,
            ifLastChange: "2023-03-01T00:00:00.000Z",
        },
    },
];

function filterChangeSchemas(changes: ChangeSchema[], searchString: string): ChangeSchema[] {
    const lowerCaseSearchString = searchString.toLowerCase();

    return changes.filter(change => {
        // Filtrar propiedades de ChangeSchema
        const matchesChangeSchema = Object.values(change).some(value => {
            if (typeof value === 'string') {
                return value.toLowerCase().includes(lowerCaseSearchString);
            }
            return false;
        });

        // Filtrar propiedades de ChangeInterfaceSchema
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

export default function HomeView() {
    const pathname = usePathname();
    const allChanges = changesExample;
    const statusOptions = [StatusAssignment.inspected, StatusAssignment.rediscovered];

    const [statusAssignment, setStatusAssignment] = useState<string | null>(null);
    const [filterContent, setFilterContent] = useState<string | null>(null);
    
    const [user, setUser] = useState<UserInfoSchema | null>(null);
    const [changesCheck, setChangesCheck] = useState<ChangeSchema[]>([]);
    const [changesFilter, setChangesFilter] = useState<ChangeSchema[]>([]);

    const addChangeCheck = (change: ChangeSchema) => {
        setChangesCheck([...changesCheck, change]);
    }

    const removeChangeCheck = (change: ChangeSchema) => {
        setChangesCheck(changesCheck.filter(c => (c.ip !== change.ip && c.community !== change.community && c.sysname !== change.sysname && c.ifIndex !== change.ifIndex)));
    }

    const filterChange = () => {
        if (filterContent && allChanges) setChangesFilter(filterChangeSchemas(allChanges, filterContent));
    }

    const handlerChangesCheck = (change: ChangeSchema, status: boolean) => {
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
        if ((statusAssignment) && (changesCheck.length > 0)) {
            console.log(statusAssignment);
            console.log(changesCheck);
        }
    }

    const getUser = async () => {
        if (sessionStorage.getItem('user')) {
            const user = JSON.parse(sessionStorage.getItem('user') as string) as UserInfoSchema;
            if (user) setUser(user);
        }
    };

    useEffect(() => {
        if (filterContent && filterContent.length > 0) filterChange();
        else setChangesFilter(allChanges);
    }, [filterContent]);
    
    useEffect(() => {
        // getUser();
        setChangesFilter(allChanges);
    }, []);

    return (
        <main className="w-full h-screen flex flex-col">
            <section className='w-full h-fit px-4 py-1 mb-4 flex flex-col gap-4'>
                <Navbar />
                {user && 
                    <h1 className='text-4xl text-white-50 font-bold px-2 md:px-8'>¡Bienvenido, <span className='italic'>{user.name} {user.lastname}!</span></h1>
                }
                {pathname === Routes.home &&
                    <div className='w-full flex flex-col items-center'>
                        <div className='w-fit'>
                            <h2 className='text-center text-3xl text-white-50 font-bold px-4'>Asignaciones</h2>
                            <div className='w-full h-1 mt-1 bg-yellow-500 rounded-full'></div>
                        </div>
                    </div>
                }
            </section>
            <section className='h-full bg-white-100 flex flex-col'>
                <div className='w-full bg-gray-950 py-3 h-fit mb-4 flex flex-col items-center justify-center gap-2'>
                    <h3 className='text-xl text-white-55 font-bold'>Seleccione las asignaciones para cambiar su estatus</h3>
                    <div className='w-full h-fit flex justify-center gap-2'>
                        <SelectorForm id='StatusAssignment' label='Estatus de Asignaciones' options={statusOptions} getValue={handlerStatus} />
                        <button 
                            onClick={handlerUpdateStatus}
                            className={`px-4 py-1 ${(changesCheck.length > 0 && statusAssignment) ? "bg-blue-800": "bg-gray-400"} rounded-full text-white-50 transition-all duration-300 ease-in-out ${(changesCheck.length > 0 && statusAssignment) ? "hover:bg-green-800": "hover:bg-gray-400"}`}>
                                Asignar Estatus
                        </button>
                    </div>
                    <FilterForm getValue={handlerFilter}/>
                </div>
                <div className={`w-full px-2 ${(changesFilter && changesFilter.length > 0) ? "h-fit" : "h-full flex flex-row items-center justify-center"}`}>
                    {changesFilter && changesFilter.length > 0 &&
                        changesFilter.map((change, index) => {
                            return <InterfaceAssignedCard key={index} data={change} handlerData={handlerChangesCheck} />
                        })
                    }
                    {(!changesFilter || changesFilter.length <= 0) &&
                        <h2 className='text-center text-2xl text-gray-400 font-bold py-4'>No hay asignaciones</h2>
                    }
                </div>
            </section>
        </main>
    );
}