'use client';
import { statics_assignments } from '@/app/example';
import PageTitles from '@app/components/titles/titlePage';
import LoadingModal from '@app/components/modals/loading';
import AlertModal from '@/app/components/modals/alert';
import Navbar from '@components/navbar/navbar';
import BarGraphGeneral from '@/app/components/graphs/barGeneral';
import BarGraphGeneralOperators from '@/app/components/graphs/barGeneralOperators';
import { DateHandler } from '@libs/date';
import { CurrentSession } from '@libs/session';
import { AssignmentStatisticsOperatorsResponseSchema, AssignmentStatisticsResponseSchema } from '@schemas/assignment';
import { AssignmentService } from '@/services/assignment';
import { useEffect, useState } from "react";

export default function StatisticsGeneralView() {
    const [loading, setLoading] = useState<boolean>(true);
    const [errorInfo, setErrorInfo] = useState<boolean>(false);

    const [generalByMonth, setGeneralByMonth] = useState<AssignmentStatisticsResponseSchema | null>(null);
    const [generalByDay, setGeneralByDay] = useState<AssignmentStatisticsResponseSchema | null>(null);
    const [generalByUsers, setGeneralByUsers] = useState<AssignmentStatisticsOperatorsResponseSchema[]>([]);
    const [generalByUsersDay, setGeneralByUsersDay] = useState<AssignmentStatisticsOperatorsResponseSchema[]>([]);
    const [generalByUsersMonth, setGeneralByUsersMonth] = useState<AssignmentStatisticsOperatorsResponseSchema[]>([]);

    const getAssignments = async () => {
        let currentToken = CurrentSession.getToken();
        let currentUser = CurrentSession.getInfoUser();
        if (currentToken && currentUser) {
            const generalByMonthData = await AssignmentService.getStatisticsGeneralByMonth(currentToken, DateHandler.getCurrentMonth());
            if (generalByMonthData) setGeneralByMonth(generalByMonthData);
            // const generalByDayData = await AssignmentService.getStatisticsGeneralByDay(currentToken, DateHandler.getCurrentDate());
            // if (generalByDayData) setGeneralByDay(generalByDayData);
            // const generalByUsersData = await AssignmentService.getStatisticsGeneralByUsers(currentToken);
            // if (generalByUsersData.length > 0) setGeneralByUsers(generalByUsersData);
            // const generalByUsersDayData = await AssignmentService.getStatisticsGeneralByUsersDay(currentToken, DateHandler.getCurrentDate());
            // if (generalByUsersDayData.length > 0) setGeneralByUsersDay(generalByUsersDayData);
            // const generalByUsersMonthData = await AssignmentService.getStatisticsGeneralByUsersMonth(currentToken, DateHandler.getCurrentMonth());
            // if (generalByUsersMonthData.length > 0) setGeneralByUsersMonth(generalByUsersMonthData);
            handlerLoading();
        } else {
            handlerLoading();
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

    useEffect(() => {
        getAssignments();
    }, []);

    return (
        <main className="w-full h-screen max-h-fit flex flex-col">
            <LoadingModal showModal={loading} />
            {errorInfo && 
                <AlertModal 
                    showModal={true} 
                    title='Error al obtener información' 
                    message='Ocurrió un error al intentar obtener la información. Por favor, refresca la página e inténtelo de nuevo. Si el error persiste, consulte a soporte.' 
                    afterAction={handlerErrorInfo}
                />
            }
            <section className='w-full h-fit px-4 py-1 mb-4 flex flex-col gap-4'>
                <Navbar />
                <PageTitles />
            </section>
            <section className='h-full bg-white-100 flex flex-col'>
                <section className='w-full h-fit mb-1'>
                    <div className='w-full bg-gray-950 py-3 h-fit mb-4 flex flex-col items-center justify-center gap-2'>
                        <div className='w-fit h-fit flex flex-row gap-3'>
                            <h3 className='text-xl text-white-55 font-bold'>Estadísticas Generales del Mes</h3>
                        </div>
                    </div>
                    <div className={`w-full px-2 ${generalByMonth ? "h-fit" : "h-72 flex flex-row items-center justify-center"} lg:px-6`}>
                        {(generalByMonth) &&
                            <BarGraphGeneral canvasID='bar-graph-1' statistics={generalByMonth} />
                        }
                        {(!generalByMonth) &&
                            <h2 className='text-center text-2xl text-gray-400 font-bold py-4'>Sin Estadísticas</h2>
                        }
                    </div>
                </section>
                <section className='w-full h-fit'>
                    <div className='w-full bg-gray-950 py-3 h-fit mb-4 flex flex-col items-center justify-center gap-2'>
                        <div className='w-fit h-fit flex flex-row gap-3'>
                            <h3 className='text-xl text-white-55 font-bold'>Estadísticas Generales del Día</h3>
                        </div>
                    </div>
                    <div className={`w-full px-2 ${generalByDay ? "h-fit" : "h-72 flex flex-row items-center justify-center"} lg:px-6`}>
                        {(generalByDay) &&
                            <BarGraphGeneral canvasID='bar-graph-2' statistics={generalByDay} />
                        }
                        {(!generalByDay) &&
                            <h2 className='text-center text-2xl text-gray-400 font-bold py-4'>Sin Estadísticas</h2>
                        }
                    </div>
                </section>
                <section className='w-full h-fit'>
                    <div className='w-full bg-gray-950 py-3 h-fit mb-4 flex flex-col items-center justify-center gap-2'>
                        <div className='w-fit h-fit flex flex-row gap-3'>
                            <h3 className='text-xl text-white-55 font-bold'>Estadísticas de Usuarios General</h3>
                        </div>
                    </div>
                    <div className={`w-full px-2 ${generalByUsers.length > 0 ? "h-fit" : "h-72 flex flex-row items-center justify-center"} lg:px-6`}>
                        {(generalByUsers.length > 0) &&
                            <BarGraphGeneralOperators canvasID='bar-graph-3' statistics={generalByUsers} />
                        }
                        {(generalByUsers.length <= 0) &&
                            <h2 className='text-center text-2xl text-gray-400 font-bold py-4'>Sin Estadísticas</h2>
                        }
                    </div>
                </section>
                <section className='w-full h-fit'>
                    <div className='w-full bg-gray-950 py-3 h-fit mb-4 flex flex-col items-center justify-center gap-2'>
                        <div className='w-fit h-fit flex flex-row gap-3'>
                            <h3 className='text-xl text-white-55 font-bold'>Estadísticas de Usuarios en el Mes</h3>
                        </div>
                    </div>
                    <div className={`w-full px-2 ${generalByUsersMonth.length > 0 ? "h-fit" : "h-72 flex flex-row items-center justify-center"} lg:px-6`}>
                        {(generalByUsersMonth.length > 0) &&
                            <BarGraphGeneralOperators canvasID='bar-graph-4' statistics={generalByUsersMonth} />
                        }
                        {(generalByUsersMonth.length <= 0) &&
                            <h2 className='text-center text-2xl text-gray-400 font-bold py-4'>Sin Estadísticas</h2>
                        }
                    </div>
                </section>
                <section className='w-full h-fit'>
                    <div className='w-full bg-gray-950 py-3 h-fit mb-4 flex flex-col items-center justify-center gap-2'>
                        <div className='w-fit h-fit flex flex-row gap-3'>
                            <h3 className='text-xl text-white-55 font-bold'>Estadísticas de Usuarios en el Día</h3>
                        </div>
                    </div>
                    <div className={`w-full px-2 ${generalByUsersDay.length > 0 ? "h-fit" : "h-72 flex flex-row items-center justify-center"} lg:px-6`}>
                        {(generalByUsersDay.length > 0) &&
                            <BarGraphGeneralOperators canvasID='bar-graph-5' statistics={generalByUsersDay} />
                        }
                        {(generalByUsersDay.length <= 0) &&
                            <h2 className='text-center text-2xl text-gray-400 font-bold py-4'>Sin Estadísticas</h2>
                        }
                    </div>
                </section>
            </section>
        </main>
    );
}