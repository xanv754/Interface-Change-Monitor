'use client';

import { revised_assignments } from '@/app/example';
import Navbar from '@components/navbar/navbar';
import InterfaceAssignedCard from '@/app/components/card/assigned';
import { Routes } from '@/libs/routes';
import { AssignmentInterfaceSchema } from '@/schemas/assignment';
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

export default function HistoryView() {
    const pathname = usePathname();

    const [assignments, setAssignments] = useState<AssignmentInterfaceSchema[]>([]);

    const handlerDownloadHistory = () => {
        console.log("Descargando historial...");
    }

    const getAssignments = async () => {
        const data = await revised_assignments;
        setAssignments(data);
    }

    useEffect(() => {
        getAssignments();
    }, []);

    return (
        <main className="w-full h-screen flex flex-col">
            <section className='w-full h-fit px-4 py-1 mb-4 flex flex-col gap-4'>
                <Navbar />
                {pathname === Routes.historyPersonal &&
                    <div className='w-full flex flex-col items-center'>
                        <div className='w-fit'>
                            <h2 className='text-center text-3xl text-white-50 font-bold px-4'>Historial</h2>
                            <div className='w-full h-1 mt-1 bg-yellow-500 rounded-full'></div>
                        </div>
                    </div>
                }
            </section>
            <section className='h-full bg-white-100 flex flex-col'>
                <div className='w-full bg-gray-950 py-3 h-fit mb-4 flex flex-col items-center justify-center gap-2'>
                    <h3 className='text-xl text-white-55 font-bold'>Descargar mi historial</h3>
                    <button 
                        onClick={handlerDownloadHistory}
                        className={`px-4 py-1 ${(assignments.length > 0) ? "bg-blue-800": "bg-gray-400"} rounded-full text-white-50 transition-all duration-300 ease-in-out ${(assignments.length > 0) ? "hover:bg-green-800": "hover:bg-gray-400"}`}>
                        Descargar
                    </button>
                </div>
                <div className={`w-full px-2 ${(assignments && assignments.length > 0) ? "h-fit" : "h-full flex flex-row items-center justify-center"}`}>
                    {assignments && assignments.length > 0 &&
                        // assignments.map((change, index) => {
                        //     return <InterfaceAssignedCard key={index} data={change} handlerData={handlerChangesCheck} />
                        // })
                        <p>Asignaciones...</p>
                    }
                    {(!assignments || assignments.length <= 0) &&
                        <h2 className='text-center text-2xl text-gray-400 font-bold py-4'>Historial Vacío</h2>
                    }
                </div>
            </section>
        </main>
    );
}