'use client';

import { statics_assignments } from '@/app/example';
import Navbar from '@components/navbar/navbar';
import BarGraphPersonal from '@/app/components/graphs/barPersonal';
import { Routes } from '@/libs/routes';
import { AssignmentStatisticsResponseSchema } from '@/schemas/assignment';
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

export default function StatisticsPersonalView() {
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
        <main className="w-full h-screen flex flex-col">
            <section className='w-full h-fit px-4 py-1 mb-4 flex flex-col gap-4'>
                <Navbar />
                {pathname === Routes.statisticsPersonal &&
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
                    <div className='w-fit flex flex-row gap-3'>
                        <h3 className='text-xl text-white-55 font-bold'>Total de Asignaciones:</h3>
                        <p className='text-xl text-white-55 font-bold'>0</p>
                    </div>
                </div>
                <div className={`w-full px-2 h-full flex flex-row items-center justify-center`}>
                    {(assignments.length > 0) &&
                        <BarGraphPersonal canvasID='bar-graph-1' data={assignments[0]} />
                    }
                    {(assignments.length <= 0) &&
                        <h2 className='text-center text-2xl text-gray-400 font-bold py-4'>Sin Estadísticas</h2>
                    }
                </div>
            </section>
        </main>
    );
}