import { months, getCurrentMonth, getCurrentYear } from "../../../utils/date";
import { ElementController } from "../../controllers/element.controller";
import { AdminController } from "../../controllers/admin.controller";
import { UserController } from "../../controllers/user.controller";
import type { InterfaceModel } from "../../models/interface";
import type { UserModel } from "../../models/user";
import type { Element } from "../../models/element";
import { Zoom, Slide } from "react-awesome-reveal";
import { useState, useEffect } from "react";

interface Props {
    token: string;
    elements: Element[];
    users: UserModel[];
}

function expandedCollapse(event) {       
    const button = event.target;
    let id = button.id;
    if ((id == 'element-collapse-1') || (id == 'content-collapse-1')) {
        const elementCollapse = document.getElementById('element-collapse-1');
        const contentCollapse = document.getElementById('content-collapse-1');

        if (elementCollapse.classList.contains('bg-gray-500')) {
            elementCollapse.classList.remove('bg-gray-500');
            elementCollapse.classList.add('bg-gray-800');
        } else {
            elementCollapse.classList.remove('bg-gray-800');
            elementCollapse.classList.add('bg-gray-500');
        }
        contentCollapse.classList.toggle('hidden');
    }
    else if ((id == 'element-collapse-2') || (id == 'content-collapse-2')) {
        const elementCollapse = document.getElementById('element-collapse-2');
        const contentCollapse = document.getElementById('content-collapse-2');

        if (elementCollapse.classList.contains('bg-gray-500')) {
            elementCollapse.classList.remove('bg-gray-500');
            elementCollapse.classList.add('bg-gray-800');
        } else {
            elementCollapse.classList.remove('bg-gray-800');
            elementCollapse.classList.add('bg-gray-500');
        }
        contentCollapse.classList.toggle('hidden');
    }
    
}

export default function ViewHistory({ token, elements, users }: Props){
    const [selectedUser, setSelectedUser] = useState<string | null>(null);
    const [user, setUser] = useState<UserModel | null>(null);
    const [totalElementsInTheMonth, setTotalElementsInTheMonth] = useState<string>(null);

    const selectedOptionsHandler = (idMember: string) => {
        if (idMember == 'General') setSelectedUser(null);
        else setSelectedUser(idMember);
    }

    useEffect(() => {
        const getTotal = async () => {
            const total = await ElementController.getTotalBackupInTheMonth(token);
            setTotalElementsInTheMonth(total);
        }
        getTotal();
    }, []);

    useEffect(() => {
        const searchUser = () => {
            users.map((user: UserModel) => {
                if (user.username == selectedUser) setUser(user);
            });
        }
        searchUser();
    }, [selectedUser]);

    return(
        <div className="min-h-fit h-full bg-blue-500 mt-4 rounded-t-3xl flex flex-row p-4 gap-2 max-sm:h-fit max-md:flex-col">
            <section id="menu" className="min-h-full w-30vw rounded-md flex flex-col max-md:w-full">
                <h1 className="font-lexend font-bold text-white text-2xl py-2">Información</h1>
                <div className="h-full w-full bg-white rounded-md pb-2 overflow-y-auto">
                    <ul className="px-2 pt-2" onClick={() => {selectedOptionsHandler('General')}}>
                        {!selectedUser && 
                            <li className="w-full p-2 text-white bg-red-500 rounded-lg transition-all duration-300 ease-in-out font-bold">General</li>
                        }
                        {selectedUser &&
                            <li className="w-full p-2 text-blue-500 bg-gray-500 rounded-lg transition-all duration-300 ease-in-out hover:bg-gray-800 hover:font-bold">General</li>
                        }
                    </ul>
                    {users &&
                        users.map((user: UserModel, index) => {
                            return(
                                <ul key={index} className="px-2 pt-2" onClick={() => {selectedOptionsHandler(user.username)}}>
                                    {!selectedUser && 
                                        <li className="w-full p-2 text-blue-500 bg-gray-500 rounded-lg transition-all duration-300 ease-in-out hover:bg-gray-800 hover:font-bold">{user.name} {user.lastname}</li>
                                    }
                                    {selectedUser && selectedUser != user.id && 
                                        <li className="w-full p-2 text-blue-500 bg-gray-500 rounded-lg transition-all duration-300 ease-in-out hover:bg-gray-800 hover:font-bold">{user.name} {user.lastname}</li>
                                    }
                                    {selectedUser && selectedUser == user.id && 
                                        <li className="w-full p-2 text-white bg-red-500 rounded-lg transition-all duration-300 ease-in-out font-bold ">{user.name} {user.lastname}</li>
                                    }
                                </ul>
                            )
                        })
                    }
                </div>
            </section>
            {!selectedUser &&
                <article id="content" className="bg-white min-h-fit h-full w-70vw rounded-md p-4 max-md:w-full overflow-y-auto">
                    <section id="title" className="h-10 w-full flex flex-col justify-start items-center mb-2">
                        <Zoom>
                            <h1 className="font-lexend font-bold text-blue-500 text-2xl mb-2">{months[Number(getCurrentMonth()) - 1]} {getCurrentYear()}</h1>
                            <div className="bg-blue-500 h-2 w-50vw rounded-full"></div>
                        </Zoom>
                    </section>
                    <Slide direction="up">
                        <section id="content" className="h-fit min-h-fit w-full flex flex-col justify-start items-start gap-2">
                            <div className="w-full h-fit flex flex-row max-sm:flex-col bg-gray-800 rounded-md">
                                <label className="h-full w-40 bg-blue-500 py-2 px-4 flex flex-wrap justify-start items-center md:rounded-l-md max-sm:rounded-t-md max-sm:justify-center max-sm:w-full max-sm:text-center">
                                    <h1 className="text-white font-bold font-lexend">Total de Interfaces con Cambios Detectados en el Mes</h1>
                                </label>
                                <div className="h-full w-60 py-2 px-6 flex flex-wrap justify-start items-center max-sm:justify-center max-sm:w-full">
                                    <p className="font-lexend">{totalElementsInTheMonth}</p>
                                </div>
                            </div>
                            <div className="w-full h-fit flex flex-row max-sm:flex-col bg-gray-800 rounded-md">
                                <label className="h-full w-40 bg-blue-500 py-2 px-4 flex flex-wrap justify-start items-center md:rounded-l-md max-sm:rounded-t-md max-sm:justify-center max-sm:w-full max-sm:text-center">
                                    <h1 className="text-white font-bold font-lexend">Total de Interfaces con Cambios Detectados en el Día</h1>
                                </label>
                                <div className="h-full w-60 py-2 px-6 flex flex-wrap justify-start items-center max-sm:justify-center max-sm:w-full">
                                    <p className="font-lexend">{elements.length}</p>
                                </div>
                            </div>
                            <div className="w-full h-fit flex flex-row max-sm:flex-col bg-gray-800 rounded-md">
                                <label className="h-full w-40 bg-blue-500 py-2 px-4 flex flex-wrap justify-start items-center md:rounded-l-md max-sm:rounded-t-md max-sm:justify-center max-sm:w-full max-sm:text-center">
                                    <h1 className="text-white font-bold font-lexend">Total de Interfaces Revisadas en el Mes</h1>
                                </label>
                                <div className="h-full w-60 py-2 px-6 flex flex-wrap justify-start items-center max-sm:justify-center max-sm:w-full">
                                    <p className="font-lexend">{AdminController.getTotalInterfaceReviewedInTheMonth(users)}</p>
                                </div>
                            </div>
                            <div className="w-full h-fit flex flex-row max-sm:flex-col bg-gray-800 rounded-md">
                                <label className="h-full w-40 bg-blue-500 py-2 px-4 flex flex-wrap justify-start items-center md:rounded-l-md max-sm:rounded-t-md max-sm:justify-center max-sm:w-full max-sm:text-center">
                                    <h1 className="text-white font-bold font-lexend">Total de Interfaces Revisadas en el Día</h1>
                                </label>
                                <div className="h-full w-60 py-2 px-6 flex flex-wrap justify-start items-center max-sm:justify-center max-sm:w-full">
                                    <p className="font-lexend">{AdminController.getTotalInterfaceReviewedInTheDay(users)}</p>
                                </div>
                            </div>
                            <div className="w-full h-fit flex flex-row max-sm:flex-col bg-gray-800 rounded-md">
                                <label className="h-full w-40 bg-blue-500 py-2 px-4 flex flex-wrap justify-start items-center md:rounded-l-md max-sm:rounded-t-md max-sm:justify-center max-sm:w-full max-sm:text-center">
                                    <h1 className="text-white font-bold font-lexend">Total de Interfaces Pendientes</h1>
                                </label>
                                <div className="h-full w-60 py-2 px-6 flex flex-wrap justify-start items-center max-sm:justify-center max-sm:w-full">
                                    <p className="font-lexend">{AdminController.getTotalInterfacePending(users)}</p>
                                </div>
                            </div>
                        </section>
                    </Slide>
                </article>
            }
            {selectedUser && user &&
                <article id="content" className="bg-white h-full w-70vw rounded-md p-4 max-md:w-full overflow-y-auto">
                    <section id="title" className="h-10 w-full flex flex-col justify-start items-center mb-6 text-center">
                        <Zoom>
                            <h1 className="font-lexend font-bold text-blue-500 text-2xl mb-2">{user.name + ' ' + user.lastname} - {months[Number(getCurrentMonth()) - 1]} {getCurrentYear()}</h1>
                            <div className="bg-blue-500 h-2 w-50vw rounded-full"></div>
                        </Zoom>
                    </section>
                    <Slide direction="up">
                        <section id="content" className="h-fit w-full flex flex-row flex-wrap justify-center items-start gap-2 max-sm:flex-col">
                            <div className="w-30 h-fit max-md:h-80 flex flex-col bg-gray-800 rounded-md max-sm:w-full">
                                <label className="h-50 bg-blue-500 py-2 px-4 flex flex-wrap items-center rounded-t-md justify-center w-full text-center">
                                    <h1 className="text-white font-bold font-lexend">Total de Interfaces Asignadas en el Mes</h1>
                                </label>
                                <div className="h-50 p-2 flex flex-wrap items-center justify-center w-full">
                                    <p className="font-lexend">{UserController.getTotalInterfaceAssignedInTheMonth(user)}</p>
                                </div>
                            </div>
                            <div className="w-30 h-fit max-md:h-80 flex flex-col bg-gray-800 rounded-md max-sm:w-full">
                                <label className="h-50 bg-blue-500 py-2 px-4 flex flex-wrap items-center rounded-t-md justify-center w-full text-center">
                                    <h1 className="text-white font-bold font-lexend">Total de Interfaces Revisadas en el Mes</h1>
                                </label>
                                <div className="h-50 p-2 flex flex-wrap items-center justify-center w-full">
                                    <p className="font-lexend">{UserController.getTotalInterfaceReviewedInTheMonth(user)}</p>
                                </div>
                            </div>
                            <div className="w-30 h-fit max-md:h-80 flex flex-col bg-gray-800 rounded-md max-sm:w-full">
                                <label className="h-50 bg-blue-500 py-2 px-4 flex flex-wrap items-center rounded-t-md justify-center w-full text-center">
                                    <h1 className="text-white font-bold font-lexend">Total de Interfaces Revisadas en el Día</h1>
                                </label>
                                <div className="h-50 p-2 flex flex-wrap items-center justify-center w-full">
                                    <p className="font-lexend">{UserController.getTotalInterfaceReviewedInTheDay(user)}</p>
                                </div>
                            </div>
                            <div className="w-30 h-fit max-md:h-80 flex flex-col bg-gray-800 rounded-md max-sm:w-full">
                                <label className="h-50 bg-blue-500 py-2 px-4 flex flex-wrap items-center rounded-t-md justify-center w-full text-center">
                                    <h1 className="text-white font-bold font-lexend">Total de Interfaces Pendientes en el Día</h1>
                                </label>
                                <div className="h-50 p-2 flex flex-wrap items-center justify-center w-full">
                                    <p className="font-lexend">{UserController.getTotalInterfacePendingInTheDay(user)}</p>
                                </div>
                            </div>
                            <section id="element-collapse-1" className="w-full h-fit text-start rounded-md p-2 bg-gray-500 flex flex-col transition-all ease-in-out duration-300 hover:bg-gray-800 focus:bg-gray-800" onClick={(e) => {expandedCollapse(e)}}>
                                <section className="w-full h-full flex flex-row">
                                    <div id="element-collapse-1" className="w-80 flex justify-start items-center">
                                        <h2 id="element-collapse-1" className="font-lexend font-bold text-blue-500">Interfaces Pendientes</h2>
                                    </div>
                                    <div id="element-collapse-1" className="w-20 flex justify-end items-center">
                                        <svg id="element-collapse-1" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#111D4A" className="bi bi-caret-down-fill" viewBox="0 0 16 16">
                                            <path id="element-collapse-1" d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                                        </svg>
                                    </div>
                                </section>
                                <div id="content-collapse-1" className="p-2 w-full hidden">
                                    {UserController.getInterfacesPending(user).length > 0 && UserController.getInterfacesPending(user).map((assignedInterface: InterfaceModel, index) => {
                                        return(
                                            <div key={index} id="content-collapse-1" className="w-full bg-gray-500 m-2 p-2 rounded-lg flex flex-row flex-wrap justify-start items-center gap-10">
                                                <h4 className="font-lexend font-normal">IP: <span className="font-light">{assignedInterface.ip}</span></h4>
                                                <h4 className="font-lexend font-normal">Comunidad: <span className="font-light">{assignedInterface.community}</span></h4>
                                                <button className="w-fit h-fit px-4 py-2 bg-blue-500 text-white text-sm font-lexend font-bold rounded-full transition-all duration-300 ease-in-out hover:bg-red-500" onClick={() => {location.href = `/detalle/${assignedInterface.idElement}`}}>Detalles</button>
                                            </div>     
                                        );
                                    })}
                                    {UserController.getInterfacesPending(user).length <= 0 &&
                                        <h2 className="text-green-800 font-lexend bg-gray-500 p-2 rounded-lg">El usuario no tiene interfaces pendientes actualmente.</h2>
                                    }
                                </div>
                            </section>
                            <section id="element-collapse-2" className="w-full h-fit text-start rounded-md p-2 bg-gray-500 flex flex-col transition-all ease-in-out duration-300 hover:bg-gray-800 focus:bg-gray-800" onClick={(e) => {expandedCollapse(e)}}>
                                <section className="w-full h-full flex flex-row">
                                    <div id="element-collapse-2" className="w-80 flex justify-start items-center">
                                        <h2 id="element-collapse-2" className="font-lexend font-bold text-blue-500">Interfaces Revisadas</h2>
                                    </div>
                                    <div id="element-collapse-2" className="w-20 flex justify-end items-center">
                                        <svg id="element-collapse-2" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#111D4A" className="bi bi-caret-down-fill" viewBox="0 0 16 16">
                                            <path id="element-collapse-2" d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                                        </svg>
                                    </div>
                                </section>
                                <div id="content-collapse-2" className="p-2 w-full hidden">
                                    {UserController.getInterfacesReviewed(user).length > 0 && UserController.getInterfacesReviewed(user).map((dataInterface: InterfaceModel, index) => {
                                        return(
                                            <div key={index} id="content-collapse-2" className="w-full bg-gray-500 m-2 p-2 rounded-lg flex flex-row flex-wrap justify-start items-center gap-10">
                                                <h4 className="font-lexend font-normal">IP: <span className="font-light">{dataInterface.ip}</span></h4>
                                                <h4 className="font-lexend font-normal">Comunidad: <span className="font-light">{dataInterface.community}</span></h4>
                                                <button className="w-fit h-fit px-4 py-2 bg-blue-500 text-white text-sm font-lexend font-bold rounded-full transition-all duration-300 ease-in-out hover:bg-red-500" onClick={() => {location.href = `/detalle/${dataInterface.idElement}`}}>Detalles</button>
                                            </div>     
                                        );
                                    })}
                                    {UserController.getInterfacesReviewed(user).length <= 0 &&
                                        <h2 className="text-red-500 font-lexend bg-gray-500 p-2 rounded-lg">El usuario no tiene interfaces revisadas actualmente.</h2>
                                    }
                                </div>
                            </section>
                        </section>
                    </Slide>
                </article>
            }
            {selectedUser && !user &&
                <article id="content" className="bg-white h-full w-70vw rounded-md p-4 max-md:w-full">
                    <div className='flex h-full w-full flex-col justify-center items-center'>
                        <img src="/assets/error.png" alt="error" className='w-10 py-4 max-sm:w-10' />
                        <h2 className='text-black-100 font-bold text-3xl max-sm:text-lg'>Error</h2>
                        <h3 className='text-black-100 max-sm:text-sm'>Ha ocurrido un error inesperado al obtener la data</h3>
                    </div>
                </article>
            }
        </div>
    );
}