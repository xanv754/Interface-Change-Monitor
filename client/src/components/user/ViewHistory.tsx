import { ElementController } from "../../controllers/element.controller";
import { getCurrentMonth } from "../../../utils/date";
import type { Element } from "../../models/element";
import { Zoom, Slide } from "react-awesome-reveal";
import type { UserModel } from "../../models/user";
import { UserController } from "../../controllers/user.controller";
import { useEffect, useState } from "react";
import type { InterfaceModel } from "../../models/interface";

interface Props {
    token: string;
    user: UserModel;
}

function setEditData(section: string) {
    let input = document.getElementById(section);
    let btnEdit = document.getElementById(`btn-${section}-edit`);
    let btnSave = document.getElementById(`btn-${section}`);
    let btnCancel = document.getElementById(`btn-${section}-cancel`);

    input.removeAttribute('disabled');
    btnSave.classList.toggle("hidden");
    btnSave.classList.toggle("flex");
    btnCancel.classList.toggle("hidden");
    btnCancel.classList.toggle("flex");
    btnEdit.classList.toggle("hidden");
    btnEdit.classList.toggle("flex");
}

function cancelEdit(section: string) {
    let input = document.getElementById(section) as HTMLInputElement;
    let btnEdit = document.getElementById(`btn-${section}-edit`);
    let btnSave = document.getElementById(`btn-${section}`);
    let btnCancel = document.getElementById(`btn-${section}-cancel`);

    input.setAttribute('disabled', '');
    input.value = "";
    btnSave.classList.toggle("hidden");
    btnSave.classList.toggle("flex");
    btnCancel.classList.toggle("hidden");
    btnCancel.classList.toggle("flex");
    btnEdit.classList.toggle("hidden");
    btnEdit.classList.toggle("flex");
}

export default function ViewData({ token, user }: Props) {

    const [interfacesPending, setInterfacesPending] = useState<InterfaceModel[]>([]);
    const [interfacesReviewed, setInterfacesReviewed] = useState<InterfaceModel[]>([]);

    const currentMonth = getCurrentMonth();

    const saveEdit = async (section: string) => {
        console.log(section);
        let input = document.getElementById(section) as HTMLInputElement;
        let btnEdit = document.getElementById(`btn-${section}-edit`);
        let btnSave = document.getElementById(`btn-${section}`);
        let btnCancel = document.getElementById(`btn-${section}-cancel`);

        input.setAttribute('disabled', '');
        btnSave.classList.toggle("hidden");
        btnSave.classList.toggle("flex");
        btnCancel.classList.toggle("hidden");
        btnCancel.classList.toggle("flex");
        btnEdit.classList.toggle("hidden");
        btnEdit.classList.toggle("flex");

        if (section == 'name') {
            const updated = await UserController.updateName(token, user.username, input.value);
            if (updated) {
                alert('Nombre actualizado');
                location.reload();
            } else {
                alert('Error al actualizar. Por favor, intente de nuevo');
            }
        } else if (section == 'lastname') {
            const updated = await UserController.updateLastname(token, user.username, input.value);
            if (updated) {
                alert('Apellido actualizado');
                location.reload();
            } else {
                alert('Error al actualizar. Por favor, intente de nuevo');
            }
        }
    }

    const downloadHandler = async () => {
        await UserController.generateDataToExcelOfInterfaceReviewed(user.assigned, currentMonth);
    }

    useEffect(() => {
        const pending = UserController.getInterfacesPending(user);
        if (pending) setInterfacesPending(pending);
        const reviewed = UserController.getInterfacesReviewed(user);
        if (reviewed) setInterfacesReviewed(reviewed);
    }, []);

    return(
        <div className="h-full min-h-fit w-full mt-4 flex flex-col gap-4 max-md:h-fit">
            <section className="w-full flex flex-row flex-wrap justify-center gap-4">
                <div className="w-20 min-w-fit text-center font-lexend bg-blue-500 text-white text-xl px-6 py-2 rounded-full">Información General</div>
            </section>
            <section className="h-full w-full min-w-fit bg-white rounded-t-3xl flex flex-row max-md:h-fit max-md:flex-col">
                <div className="h-full w-50 p-6 flex flex-col gap-4 max-md:w-full max-md:h-fit">
                    <Zoom>
                        <div className="w-full h-fit flex flex-col items-center">
                            <h2 className="font-lexend text-blue-500 font-bold text-2xl">Datos de Usuario</h2>
                            <div className="h-1 rounded-full bg-blue-500 w-40"></div>
                        </div>
                        <div className="h-full w-full min-w-fit p-6 bg-gray-550 flex flex-col items-center gap-2 rounded-xl">
                            <div className="w-full flex flex-row max-md:w-full max-md:flex-col">
                                <label className="w-30 font-lexend text-center font-bold text-white bg-blue-500 px-4 py-2 md:rounded-l-md max-md:rounded-t-md max-md:w-full">Nombre</label>
                                <input id="name" className="min-w-fit w-full font-lexend font-bold text-black-500 bg-white px-4 py-2 placeholder-blue-500 md:rounded-r-md max-md:rounded-b-md" placeholder={user.name} disabled/>
                                <button id="btn-name-edit" onClick={() => {setEditData('name')}} className='flex flex-row justify-center items-center bg-blue-500 rounded-md p-2 md:ml-1 text-white font-lexend font-medium transition-all duration-300 ease-in-out hover:bg-blue-800 max-md:mt-2'>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-pencil-square" viewBox="0 0 16 16">
                                        <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                        <path fillRule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                                    </svg>
                                </button>
                                <button id="btn-name-cancel" onClick={() => {cancelEdit('name')}} className='flex-row justify-center items-center hidden bg-blue-500 rounded-md p-2 md:ml-1 text-white font-lexend font-medium transition-all duration-300 ease-in-out hover:bg-red-500 max-md:mt-2'>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-x" viewBox="0 0 16 16">
                                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                                    </svg>
                                </button>
                                <button id="btn-name" onClick={() => {saveEdit('name')}} className='flex-row justify-center items-center hidden bg-blue-500 rounded-md p-2 md:ml-1 text-white font-lexend font-medium transition-all duration-300 ease-in-out hover:bg-green-500 max-md:mt-2'>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" className="bi bi-check-lg" viewBox="0 0 16 16">
                                        <path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425z"/>
                                    </svg>
                                </button>
                            </div>
                            <div className="w-full flex flex-row max-md:w-full max-md:flex-col">
                                <label className="w-30 font-lexend text-center font-bold text-white bg-blue-500 px-4 py-2 md:rounded-l-md max-md:rounded-t-md max-md:w-full">Apellido</label>
                                <input id="lastname" className="min-w-fit w-full font-lexend font-bold text-black-500 bg-white px-4 py-2 placeholder-blue-500 md:rounded-r-md max-md:rounded-b-md" placeholder={user.lastname} disabled/>
                                <button id="btn-lastname-edit" onClick={() => {setEditData('lastname')}} className='flex flex-row justify-center items-center bg-blue-500 rounded-md p-2 md:ml-1 text-white font-lexend font-medium transition-all duration-300 ease-in-out hover:bg-blue-800 max-md:mt-2'>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-pencil-square" viewBox="0 0 16 16">
                                        <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
                                        <path fillRule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
                                    </svg>
                                </button>
                                <button id="btn-lastname-cancel" onClick={() => {cancelEdit('lastname')}} className='flex-row justify-center items-center hidden bg-blue-500 rounded-md p-2 md:ml-1 text-white font-lexend font-medium transition-all duration-300 ease-in-out hover:bg-red-500 max-md:mt-2'>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-x" viewBox="0 0 16 16">
                                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                                    </svg>
                                </button>
                                <button id="btn-lastname" onClick={() => {saveEdit('lastname')}} className='flex-row justify-center items-center hidden bg-blue-500 rounded-md p-2 md:ml-1 text-white font-lexend font-medium transition-all duration-300 ease-in-out hover:bg-green-500 max-md:mt-2'>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="white" className="bi bi-check-lg" viewBox="0 0 16 16">
                                        <path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425z"/>
                                    </svg>
                                </button>
                            </div>
                            <div className="w-full flex flex-row max-md:w-full max-md:flex-col">
                                <label className="w-30 font-lexend text-center font-bold text-white bg-blue-500 px-4 py-2 md:rounded-l-md max-md:rounded-t-md max-md:w-full">Usuario</label>
                                <div className="min-w-fit w-full font-lexend font-bold text-black-500 bg-white px-4 py-2 md:rounded-r-md max-md:rounded-b-md">{user.username}</div>
                            </div>
                            <div className="w-full flex flex-row max-md:w-full max-md:flex-col">
                                <label className="w-30 font-lexend text-center font-bold text-white bg-blue-500 px-4 py-2 md:rounded-l-md max-md:rounded-t-md max-md:w-full">Tipo de Usuario</label>
                                <div className="min-w-fit w-full font-lexend font-bold text-black-500 bg-white px-4 py-2 md:rounded-r-md max-md:rounded-b-md">{user.type}</div>
                            </div>
                            <div className="w-full flex flex-row max-md:w-full max-md:flex-col">
                                <label className="w-60 font-lexend text-center font-bold text-white bg-blue-500 px-4 py-2 md:rounded-l-md max-md:rounded-t-md max-md:w-full">Total de Interfaces Revisadas</label>
                                <div className="min-w-fit w-full font-lexend font-bold text-black-500 bg-white px-4 flex flex-col justify-center py-2 md:rounded-r-md max-md:rounded-b-md">{interfacesReviewed.length}</div>
                            </div>
                            <div className="w-full flex flex-row max-md:w-full max-md:flex-col">
                                <label className="w-60 font-lexend text-center font-bold text-white bg-blue-500 px-4 py-2 md:rounded-l-md max-md:rounded-t-md max-md:w-full">Total de Interfaces Pendientes</label>
                                <div className="min-w-fit w-full font-lexend font-bold text-black-500 bg-white px-4 flex flex-col justify-center py-2 md:rounded-r-md max-md:rounded-b-md">{interfacesPending.length}</div>
                            </div>
                            <div className="w-full flex flex-row gap-4 justify-center items-center mt-4 max-md:w-full max-md:flex-col max-md:gap-2">
                                <h4 className="font-lexend font-bold text-blue-500 text-lg">Descarga de mi Historial</h4>
                                <button className="font-lexend bg-blue-500 font-bold text-white px-6 py-2 rounded-full transition-all duration-300 ease-in-out hover:bg-blue-800 max-sm:w-full" onClick={() => {downloadHandler()}}>Descargar</button>
                                <button className="font-lexend bg-blue-500 font-bold text-white px-6 py-2 rounded-full transition-all duration-300 ease-in-out hover:bg-blue-800 max-sm:w-full" onClick={() => {location.href = '/setPassword'}}>Cambiar Contraseña</button>
                            </div>
                        </div>
                    </Zoom>
                </div>
                <div className="h-full w-50 p-6 flex flex-col gap-4 max-md:w-full max-md:h-fit">
                    <Zoom>
                        <div className="w-full h-fit flex flex-col items-center">
                            <h2 className="font-lexend text-blue-500 font-bold text-2xl">Interfaces Revisadas</h2>
                            <div className="h-1 rounded-full bg-blue-500 w-40"></div>
                        </div>
                        <div className="h-full w-full min-w-fit p-6 bg-gray-550 flex flex-col items-center gap-2 rounded-xl overflow-y-auto">
                            {interfacesReviewed.length > 0 && 
                                <ul className="w-full max-h-96">
                                    {interfacesReviewed.map((element: InterfaceModel, index) => {
                                        return(
                                            <li key={index} className="bg-gray-600 h-fit flex flex-col gap-2 rounded-md px-6 py-2 mb-1">
                                                <div className="flex flex-row flex-wrap gap-2">
                                                    <h4 className="font-lexend font-bold text-blue-500">IP:</h4>
                                                    <p className="font-lexend font-bold text-black-500">{element.ip}</p>
                                                </div>
                                                <div className="flex flex-row flex-wrap gap-2">
                                                    <h4 className="font-lexend font-bold text-blue-500">Comunidad:</h4>
                                                    <p className="font-lexend font-bold text-black-500">{element.community}</p>
                                                </div>
                                                <div className="flex flex-row flex-wrap items-center gap-2">
                                                    <h4 className="font-lexend font-bold text-blue-500">Estatus:</h4>
                                                    <p className="font-lexend font-bold text-black-500">{element.assignment.status}</p>
                                                </div>
                                                <div className="flex flex-row justify-center items-center">
                                                    <button className="w-30 min-w-fit font-lexend bg-blue-500 font-bold text-white text-xs px-10 py-2 rounded-full transition-all duration-300 ease-in-out hover:bg-blue-800 max-sm:w-full" onClick={() => {location.href = `/detalle/${element.idElement}`}}>Detalles</button>
                                                </div>
                                            </li>
                                        );
                                    })}
                                </ul>
                            }
                            {interfacesReviewed.length <= 0 &&
                                <h3 className="font-lexend text-black-500">Sin interfaces revisadas</h3>
                            }
                        </div>
                    </Zoom>
                </div>
            </section>
        </div>
    );
}