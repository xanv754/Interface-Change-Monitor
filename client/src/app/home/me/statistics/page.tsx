'use client';

import Navbar from '@components/navbar/navbar';
import LoadingModal from '@/app/components/modals/loading';
import AlertModal from '@/app/components/modals/alert';
import PageTitles from '@/app/components/titles/titlePage';
import BarGraphPersonal from '@/app/components/graphs/barPersonal';
import { CurrentSession } from '@/libs/session';
import { AssignmentService } from '@/services/assignment';
import { DateHandler } from '@libs/date';
import { AssignmentStatisticsResponseSchema } from '@/schemas/assignment';
import { UserShortInfoResponseSchema } from "@schemas/user";
import { useEffect, useState } from "react";

export default function StatisticsPersonalView() {
    const currentDate = DateHandler.getCurrentDate();
    const currentMonth = DateHandler.getCurrentMonth();

    const [loading, setLoading] = useState<boolean>(true);
    const [errorInfo, setErrorInfo] = useState<boolean>(false);

    const [user, setUser] = useState<UserShortInfoResponseSchema | null>(null);

    const [statisticsGeneral, setStatisticsGeneral] = useState<AssignmentStatisticsResponseSchema | null>(null);
    const [statisticsByDay, setStatisticsByDay] = useState<AssignmentStatisticsResponseSchema | null>(null);
    const [statisticsByMonth, setStatisticsByMonth] = useState<AssignmentStatisticsResponseSchema | null>(null);
   
    /**
     * Get the information of the user logged in and your pending assignments.
     */
    const getData = async () => {
        let currentUser = CurrentSession.getInfoUser();
        let currentToken = CurrentSession.getToken();
        if (currentUser && currentToken) {
            setUser(currentUser);
            const dataGeneral = await AssignmentService.getStatisticsUser(currentToken);
            if (dataGeneral) setStatisticsGeneral(dataGeneral);
            const dataByDay = await AssignmentService.getStatisticsUserByDay(currentToken, currentDate);
            if (dataByDay) setStatisticsByDay(dataByDay);
            const dataByMonth = await AssignmentService.getStatisticsUserByMonth(currentToken, currentMonth);
            if (dataByMonth) setStatisticsByMonth(dataByMonth);
            handlerLoading(false);
        }
        else {
            handlerLoading(false);
            handlerErrorInfo(true);
        }
    };

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
            <section id='header' className='w-full h-fit px-4 py-1 mb-4 flex flex-col gap-4'>
                <Navbar />
                <PageTitles />
            </section>
            <section id='content' className={`w-full ${statisticsGeneral ? 'min-h-fit h-full' : 'h-full'} bg-white-100 flex flex-col`}>
                <div id='content-header' className='w-full bg-gray-950 py-3 h-fit flex flex-col items-center justify-center gap-2'>
                    {user && statisticsGeneral &&
                        <div className='w-fit flex flex-row gap-3'>
                            <h3 className='text-lg text-white-55 font-bold'>Total de Asignaciones:</h3>
                            <p className='text-xl text-white-55 font-bold'>{statisticsGeneral.totalPending + statisticsGeneral.totalRevised}</p>
                        </div>
                    }
                </div>
                {user &&
                    <div id='statistics' className='h-fit'>
                        <div id='general' className='w-full bg-gray-950 py-3 h-fit mb-4 flex flex-col items-center justify-center gap-2'>
                            <h3 id='label-statistics-general' className='text-xl text-white-55 font-bold'>Estadístiscas de Asignaciones Globales</h3>
                        </div>
                        <section id="statistics-general" className='w-full h-fit mb-2 px-2 flex flex-row items-start justify-center'>
                            {statisticsGeneral &&
                                <BarGraphPersonal canvasID='graph-general' data={statisticsGeneral} />
                            }
                            {!statisticsGeneral &&
                                <h2 id='no-statistics-general' className='text-center text-2xl text-gray-400 font-bold py-4'>Sin Estadísticas</h2>
                            }
                        </section>
                        <div id='by-day' className='w-full bg-gray-950 py-3 h-fit mb-4 flex flex-col items-center justify-center gap-2'>
                            <h3 id='label-statistics-by-day' className='text-xl text-white-55 font-bold'>Estadístiscas de Asignaciones Del Día Actual</h3>
                        </div>
                        <section id="statistics-by-day" className='w-full h-fit mb-2 px-2 flex flex-row items-start justify-center'>
                            {statisticsByDay &&
                                <BarGraphPersonal canvasID='graph-by-day' data={statisticsByDay} />
                            }
                            {!statisticsByDay &&
                                <h2 id='no-statistics-by-day' className='text-center text-2xl text-gray-400 font-bold py-4'>Sin Estadísticas</h2>
                            }
                        </section>
                        <div id='by-month' className='w-full bg-gray-950 py-3 h-fit mb-4 flex flex-col items-center justify-center gap-2'>
                            <h3 id='label-statistics-by-month' className='text-xl text-white-55 font-bold'>Estadístiscas de Asignaciones Del Mes Actual</h3>
                        </div>
                        <section id="statistics-by-month" className='w-full h-fit mb-2 px-2 flex flex-row items-start justify-center'>
                            {statisticsByMonth &&
                                <BarGraphPersonal canvasID='graph-by-month' data={statisticsByMonth} />
                            }
                            {!statisticsByMonth &&
                                <h2 id='no-statistics-by-month' className='text-center text-2xl text-gray-400 font-bold py-4'>Sin Estadísticas</h2>
                            }
                        </section>
                    </div>
                }
                {!user &&
                    <div id='content-error' className='w-full px-2 h-full flex flex-row items-center justify-center'>
                        <h2 id='content-message-error' className='text-center text-2xl text-gray-400 font-bold py-4'>Error al obtener información de usuario</h2>
                    </div>
                }
            </section>
        </main>
    );
}