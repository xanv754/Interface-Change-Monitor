'use client';

import { revised_assignments, users_example } from '@/app/example';
import Navbar from '@components/navbar/navbar';
import InterfaceAssignedCard from '@/app/components/cards/assigned';
import HistoryOperatorCard from '@/app/components/cards/historyOperator';
import InputCalendarForm from '@/app/components/forms/inputCalendar';
import { Routes } from '@/libs/routes';
import { AssignmentInfoResponseSchema } from '@/schemas/assignment';
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { convertText } from '@/libs/convert';
import { UserResponseSchema } from "@/schemas/user";

export default function HistoryGeneralView() {
    const pathname = usePathname();

    const [assignments, setAssignments] = useState<AssignmentInfoResponseSchema[]>([]);
    const [allUsers, setAllUsers] = useState<UserResponseSchema[]>([]);
    const [usersMonth, setUsersMonth] = useState<UserResponseSchema[]>([]);
    const [selectMonth, setSelectMonth] = useState<string | null>(null);

    const getUsersMonth = async () => {
        const data = await users_example;
        setUsersMonth(data);
    }

    const handlerDownloadHistory = () => {
        console.log("Descargando historial...");
    }

    const handlerSelectMonth = (month: string) => {
        setSelectMonth(month);
    }

    const getAssignments = async () => {
        const data = await revised_assignments;
        setAssignments(data);
    }

    const getUsers = async () => {
        const data = await users_example;
        setAllUsers(data);
    }

    useEffect(() => {
        if (selectMonth) getUsersMonth();
    }, [selectMonth]);

    useEffect(() => {
        getAssignments();
        getUsers();
    }, []);

    return (
        <main className="w-full h-screen flex flex-col">
            <section className='w-full h-fit px-4 py-1 mb-4 flex flex-col gap-4'>
                <Navbar />
                {pathname === Routes.historyGeneral &&
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
                    <h3 className='text-xl text-white-55 font-bold'>Descargar Cambios Encontrados de Hoy</h3>
                    <button 
                        onClick={handlerDownloadHistory}
                        className={`px-4 py-1 ${(assignments.length > 0) ? "bg-blue-800": "bg-gray-400"} rounded-full text-white-50 transition-all duration-300 ease-in-out ${(assignments.length > 0) ? "hover:bg-green-800": "hover:bg-gray-400"}`}>
                        Descargar
                    </button>
                    <h3 className='text-xl text-white-55 font-bold'>Descarga de Historial de Asignaciones Revisadas por los Usuarios</h3>
                    <InputCalendarForm id="input-calendar" label="Mes a descargar" getValue={handlerSelectMonth} disabled={allUsers && allUsers.length <= 0} />
                </div>
                <div className={`w-full px-2 ${(allUsers.length > 0 && selectMonth && usersMonth.length > 0) ? "flex flex-row gap-2" : "h-full flex flex-row items-center justify-center"}`}>               
                    {allUsers.length <= 0 &&
                        <h2 className='text-center text-2xl text-gray-400 font-bold py-4'>Historial Vacío</h2>
                    }
                    {allUsers.length > 0 && !selectMonth &&
                        <h2 className='text-center text-2xl text-gray-400 font-bold py-4'>Esperando selección del mes...</h2>
                    }
                    {allUsers.length > 0 && selectMonth && usersMonth.length > 0 &&
                        allUsers.map((user: UserResponseSchema, index: number) => {
                            return <HistoryOperatorCard key={index} user={user} getValue={handlerSelectMonth} />
                        })
                    }
                    {allUsers.length > 0 && selectMonth && usersMonth.length <= 0 &&
                        <h2 className='text-center text-2xl text-gray-400 font-bold py-4'>Sin historial para {convertText.convertMonthToText(selectMonth)}</h2>
                    }
                </div> 
            </section>
        </main>
    );
}