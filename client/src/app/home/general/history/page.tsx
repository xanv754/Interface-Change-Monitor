'use client';

import { revised_assignments, users_example } from '@app/example';
import Navbar from '@components/navbar/navbar';
import PageTitles from '@app/components/titles/titlePage';
import LoadingModal from '@app/components/modals/loading';
import AlertModal from '@/app/components/modals/alert';
import InterfaceAssignedCard from '@app/components/cards/assigned';
import HistoryOperatorCard from '@app/components/cards/historyOperator';
import InputCalendarForm from '@app/components/forms/inputCalendar';
import { CurrentSession } from '@/libs/session';
import { ExcelHandler } from '@libs/excel';
import { AssignmentHandler } from '@libs/assignment';
import { convertText as convertData } from '@libs/convert';
import { AssignmentInfoResponseSchema } from '@schemas/assignment';
import { ChangeResponseSchema } from '@/schemas/changes';
import { UserResponseSchema, UserShortInfoResponseSchema } from "@schemas/user";
import { AssignmentService } from '@/services/assignment';
import { AdministrationService } from '@/services/administration';
import { useEffect, useState } from "react";

export default function HistoryGeneralView() {
    const [loading, setLoading] = useState<boolean>(true);
    const [errorInfo, setErrorInfo] = useState<boolean>(false);
    const [errorFile, setErrorFile] = useState<boolean>(false);

    const [token, setToken] = useState<string | null>(null);

    const [changesOfDay, setChangesOfDay] = useState<ChangeResponseSchema[]>([]);
    const [assignmentsByMonth, setAssignmentsByMonth] = useState<AssignmentInfoResponseSchema[]>([]);
    const [usersWithHistory, setUsersWithHistory] = useState<UserShortInfoResponseSchema[]>([]);
    const [selectMonth, setSelectMonth] = useState<string | null>(null);
    const [selectUser, setSelectUser] = useState<string | null>(null);

    /**
     * Get the information of the user logged in.
     */
    const getData = async () => {
        let currentToken = CurrentSession.getToken();
        if (currentToken) {
            setToken(currentToken)
            const dataChanges = await AdministrationService.getChanges(currentToken);
            if (dataChanges) setChangesOfDay(dataChanges);
            handlerLoading(false);
        }
        else {
            handlerLoading(false);
            setErrorInfo(true);
        }
    };

    /**
     * Get all assignments on the selected month.
     * 
     * @param {string} token Token of the user logged in.
     */
    const getAssignmentsByMonth = async () => {
        if (token && selectMonth) {
            let month = selectMonth.split('-')[1];
            const data = await AssignmentService.getRevisedsByMonth(token, month);
            console.log("data", data);
            if (data.length > 0) setAssignmentsByMonth(data);
            handlerLoading(false);
        } else {
            handlerLoading(false);
            setErrorInfo(true);
        }
    }

    const getUserWithHistory = () => {
        if (assignmentsByMonth.length > 0) {
            setUsersWithHistory(AssignmentHandler.getUserWithHistory(assignmentsByMonth));
        };
    }

    /**
     * Handler to disable the display of the loading modal.
     * 
     * @param {boolean} displayModal If the loading modal is displayed or not.
     */
    const handlerLoading = (displayModal: boolean = false) => {
        if (displayModal) setLoading(displayModal);
        else {
            setTimeout(() => {
                setLoading(displayModal);
            }, 1000);
        }
    }

    /**
     * Handler for user error file status.
     * 
     * @param {boolean} isThereAnError If there is an error or not.
     */
    const handlerErrorFile = (isThereAnError: boolean = false) => {
        setErrorFile(isThereAnError);
    }

    /**
     * Handler to download all the changes detected on the day.
     */
    const handlerDownloadHistory = () => {
        if (selectUser && assignmentsByMonth.length > 0) {
            let dataUser = AssignmentHandler.filterAssignmentsByUser(assignmentsByMonth, selectUser);
            if (dataUser.length > 0) {
                let status = ExcelHandler.getHistoryOfUser(selectUser, dataUser);
                if (!status) handlerErrorFile(true);
            }
        }
    }

    /**
     * Handler to get selected month.
     * 
     * @param {string} month The month to select.
     */
    const handlerSelectMonth = (month: string) => {
        setSelectMonth(month);
    }

    /**
     * Handler to get selected user.
     * 
     * @param {string} username The username to select.
     */
    const handlerSelectUser = (username: string) => {
        setSelectUser(username);
    }

    useEffect(() => {
        const getHistory = async () => {
            handlerLoading(true);
            if (selectMonth) {
                await getAssignmentsByMonth();
                getUserWithHistory();
                handlerLoading(false);
            }
        }
        getHistory();
    }, [selectMonth]);

    useEffect(() => {
        handlerDownloadHistory();
    }, [selectUser]);

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
                    message='Ocurrió un error al intentar obtener el historial. Por favor, inténtelo de nuevo más tarde.' 
                />
            }
            {errorFile && 
                <AlertModal 
                    showModal={true} 
                    title='Error al generar el archivo' 
                    message='Ocurrió un error al generar el historial del usuario. Por favor, inténtelo de nuevo más tarde.'
                    afterAction={handlerErrorFile}
                />
            }
            <section id='header' className='w-full h-fit px-4 py-1 mb-4 flex flex-col gap-4'>
                <Navbar />
                <PageTitles />
            </section>
            <section id='content' className='h-full bg-white-100 flex flex-col'>
                <div id='content-header' className='w-full bg-gray-950 py-3 h-fit mb-4 flex flex-col items-center justify-center gap-2'>
                    <h3 id='label-download-history' className='text-xl text-white-55 font-bold'>Descargar Cambios Encontrados de Hoy</h3>
                    <button 
                        id='download-history'
                        onClick={handlerDownloadHistory}
                        className={`px-4 py-1 ${(changesOfDay.length > 0) ? "bg-blue-800": "bg-gray-400"} rounded-full text-white-50 transition-all duration-300 ease-in-out ${(changesOfDay.length > 0) ? "hover:bg-green-800": "hover:bg-gray-400"}`}>
                        Descargar
                    </button>
                    <h3 id='label-download-history-by-user' className='text-xl text-white-55 font-bold'>Descarga de Historial de Asignaciones Revisadas por los Usuarios</h3>
                    <InputCalendarForm id="input-calendar" label="Mes a descargar" getValue={handlerSelectMonth} />
                </div>
                <div id='data-history-by-user' className={`w-full px-2 ${(selectMonth && assignmentsByMonth.length > 0) ? "flex flex-row gap-2" : "h-full flex flex-row items-center justify-center"}`}>               
                    {!selectMonth &&
                        <h2 id='waiting-value-calendar' className='text-center text-2xl text-gray-400 font-bold py-4'>Esperando selección del mes...</h2>
                    }
                    {!loading && selectMonth && assignmentsByMonth.length > 0 && usersWithHistory.length > 0 &&
                        usersWithHistory.map((user: UserShortInfoResponseSchema, index: number) => {
                            return <HistoryOperatorCard key={index} getValue={handlerSelectUser} username={user.username} name={user.name} lastname={user.lastname} />
                        })
                    }
                    {!loading && selectMonth && assignmentsByMonth.length <= 0 &&
                        <h2 id='without-data-month' className='text-center text-2xl text-gray-400 font-bold py-4'>Sin historial para {convertData.MonthToText(selectMonth)}</h2>
                    }
                </div> 
            </section>
        </main>
    );
}