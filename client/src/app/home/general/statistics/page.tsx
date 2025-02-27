'use client';

import { statics_assignments } from '@/app/example';
import Navbar from '@components/navbar/navbar';
import BarGraphGeneral from '@/app/components/graphs/barGeneral';
import { Routes } from '@/libs/routes';
import { AssignmentStatisticsResponseSchema } from '@/schemas/assignment';
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

export default function StatisticsGeneralView() {
    const pathname = usePathname();

    const [assignments, setAssignments] = useState<AssignmentStatisticsResponseSchema[]>([]);

    const getAssignments = async () => {
        const data = await statics_assignments;
        setAssignments(data);
    }

    useEffect(() => {
        getAssignments();
    }, []);

    return (
        <main className="w-full h-screen max-h-fit flex flex-col">
            <section className='w-full h-fit px-4 py-1 mb-4 flex flex-col gap-4'>
                <Navbar />
                {pathname === Routes.statisticsGeneral &&
                    <div className='w-full flex flex-col items-center'>
                        <div className='w-fit'>
                            <h2 className='text-center text-3xl text-white-50 font-bold px-4'>Estadísticas</h2>
                            <div className='w-full h-1 mt-1 bg-yellow-500 rounded-full'></div>
                        </div>
                    </div>
                }
            </section>
            <section className='h-full bg-white-100 flex flex-col'>
                <div className='w-full bg-gray-950 py-3 h-fit mb-4 flex flex-col items-center justify-center gap-2'>
                    <div className='w-fit h-fit flex flex-row gap-3'>
                        <h3 className='text-xl text-white-55 font-bold'>Estadística por Usuarios</h3>
                    </div>
                </div>
                <div className={`w-full px-2 ${assignments.length > 0 ? "h-fit" : "h-full flex flex-row items-center justify-center"} lg:px-6`}>
                    {(assignments.length > 0) &&
                        <BarGraphGeneral canvasID='bar-graph-1' statistics={assignments} />
                    }
                    {(assignments.length <= 0) &&
                        <h2 className='text-center text-2xl text-gray-400 font-bold py-4'>Sin Estadísticas</h2>
                    }
                </div>
            </section>
        </main>
    );
}