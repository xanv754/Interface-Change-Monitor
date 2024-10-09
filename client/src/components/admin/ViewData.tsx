import { ElementController } from "../../controllers/element.controller";
import { AdminController } from "../../controllers/admin.controller";
import { UserController } from "../../controllers/user.controller";
import type { Element } from "../../models/element";
import { Zoom, Slide } from "react-awesome-reveal";
import type { UserModel } from "../../models/user";
import { useEffect, useState } from "react";

interface Props {
    elements: Element[];
    users: UserModel[];
}

export default function ViewData({ elements, users }: Props){
    const [selectMonth, setSelectMonth] = useState<string>('Ninguno');
    const [usersFilter, setUsersFilter] = useState<UserModel[]>([]);
    const [monthAvailable, setMonthAvailable] = useState<Array<{"monthString": string, "monthNumber": string}>>([]);

    const changeMonthHandler = (e) => {
        let selectedMonth = e.target.value;
        setSelectMonth(selectedMonth);
    }

    const downloadDataTodayHandler = async () => {
        await ElementController.generateDataToExcel(elements);
    }

    const downloadDataOfUserHandler = async (user: UserModel) => {
        await UserController.generateDataToExcelOfInterfaceReviewed(user.assigned, selectMonth);
    }

    useEffect(() => {
        if (selectMonth != 'Ninguno') {
            let newUsersFilter = AdminController.getUsersWithInterfacesReviewedInTheMonth(users, selectMonth);
            console.log(newUsersFilter);
            setUsersFilter(newUsersFilter);
        }
    }, [selectMonth]);

    useEffect(() => {
        const monthsData = AdminController.getMonthsOfUserData(users);
        setMonthAvailable(monthsData);
    }, []);

    return(
        <div className="h-full w-full rounded-t-2xl p-4 flex bg-blue-500 mt-4 flex-col gap-2 max-md:h-fit">
            <section className="h-10vh w-full bg-white rounded-xl px-4 flex flex-row justify-center items-center gap-4 max-md:flex-col py-10 max-md:h-fit max-md:text-center">
                {elements.length > 0 &&
                    <Slide direction="down">
                        <h2 className="font-lexend text-blue-500 font-medium text-2xl">Data con los cambios de interfaces de red de hoy</h2>
                        <button className="w-fit h-fit px-6 py-2 rounded-full bg-blue-500 text-white font-lexend font-bold transition-all duration-300 ease-in-out hover:bg-blue-800" onClick={() => downloadDataTodayHandler()}>Descargar</button>
                    </Slide>
                }
                {elements.length <= 0 &&
                    <Slide direction="down">
                        <h2 className="font-lexend text-gray-900 font-medium text-2xl">No existen cambios de interfaces hoy</h2>
                    </Slide>
                }
            </section>
            <section className="h-full w-full flex flex-col justify-start items-start py-2 gap-2">
                <div className="w-full flex flex-row max-md:flex-col">
                    <label htmlFor="select-Month" className="font-lexend text-blue-500 font-medium bg-gray-600 py-2 md:px-6 md:rounded-l-xl max-md:rounded-t-xl max-md:w-full max-md:text-center">Meses Disponibles</label>
                    <select name="select-Month" id="select-Month" className="h-full p-2 md:w-20 md:rounded-r-xl max-md:w-full max-md:rounded-b-xl" onClick={(e) => { changeMonthHandler(e) }}>
                        <option value="Ninguno">----</option>
                        {monthAvailable.length > 0 &&
                            monthAvailable.map((month, index) => {
                                return (
                                    <option key={index} value={month.monthNumber}>{month.monthString}</option>
                                )
                            })
                        }
                    </select>
                </div>
                <div className="bg-white w-full h-full rounded-xl px-8 py-6">
                    <Zoom><h2 className="font-lexend text-blue-500 text-xl font-bold text-center mb-2">Data de Usuarios</h2></Zoom>
                    <div className="h-1 w-full bg-blue-500 mb-4"></div>
                    {selectMonth == 'Ninguno' &&
                        <div className="w-full h-85 bg-gray-500 rounded-xl flex justify-center items-center px-6 py-20 max-md:h-fit">
                            <Zoom><h3 className="font-lexend text-2xl text-center font-medium text-gray-900 max-sm:text-sm max-md:text-lg">Ningún mes seleccionado</h3></Zoom>
                        </div>
                    }
                    {selectMonth != 'Ninguno' && usersFilter.length > 0 &&
                        <ul className="bg-gray-500 h-85 max-h-fit rounded-xl p-6 w-full grid grid-cols-3 gap-4 max-md:grid-cols-2 max-sm:grid-cols-1 max-md:h-fit overflow-y-auto">
                            {usersFilter.map((user: UserModel, index) => {
                                    return(
                                        <Zoom key={index}>
                                            <li className="flex flex-col gap-2 items-center max-md:flex-col max-md:justify-center">
                                                <p className="font-lexend text-blue-500 text-lg text-center">Data de interfaces de {user.name} {user.lastname}</p>
                                                <button className="font-lexend text-white bg-blue-500 px-4 py-2 rounded-full transition-all ease-in-out duration-300 hover:bg-blue-800" onClick={() => { downloadDataOfUserHandler(user) }}>Descargar</button>
                                            </li>
                                        </Zoom>
                                    );
                                })
                            }
                        </ul>
                    }
                    {selectMonth != 'Ninguno' && usersFilter.length <= 0 &&
                        <div className="w-full h-85 bg-gray-500 rounded-xl flex justify-center items-center px-6 py-20 max-md:h-fit">
                            <Zoom><h3 className="font-lexend text-2xl text-center font-bold text-gray-800 max-sm:text-sm max-md:text-lg">Ningún usuario tiene data para el mes seleccionado</h3></Zoom>
                        </div>
                    }
                </div>
            </section>
        </div>
    )
}