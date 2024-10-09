import { LoginController } from "../../controllers/login.controller";
import type { AdminModel } from "../../models/admin";
import type { UserModel } from "../../models/user";
import { useEffect, useState } from "react";

interface Props {
    token: string;
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

export default function ContainerProfile({ token }: Props) {

    const [user, setUser] = useState<AdminModel | UserModel>(null);
    const [error, setError] = useState<boolean>(false);
    const [isLoading, setLoading] = useState<boolean>(true);

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

    }

    useEffect(() => {
        const getData = async () => {
            const data = await LoginController.getDataUser(token);
            if (!data) setError(true);
            else setUser(data);
            setLoading(false);
        }
        getData();
    }, []);

    return(
        <div className="h-full w-full mt-4 bg-blue-500 rounded-t-2xl p-4">
            <div className="h-full w-full bg-gray-550 rounded-xl flex flex-col items-center p-4">
                <h2 className="font-lexend font-bold text-3xl text-blue-500">Datos de Usuario</h2>
                <div className="h-1 rounded-full bg-blue-500 w-full mt-2"></div>
                {!isLoading && error &&
                    <div className="w-full h-full flex flex-col justify-center items-center">
                        <img src="/assets/error.png" alt="" className='w-14 py-4' />
                        <h3 className="font-lexend font-bold text-2xl text-gray-900">Error al obtener los datos de usuario</h3>
                    </div>
                }
                {!isLoading && !error &&
                    <section className=" flex flex-col py-4 w-40 gap-3">
                        <div className="flex flex-row max-md:flex-col">
                            <label className="w-30 font-lexend text-center font-bold text-white bg-blue-500 px-4 py-2 md:rounded-l-md max-md:rounded-t-md max-md:w-full">Nombre</label>
                            <input id="name" className="w-full font-lexend font-bold text-black-500 bg-white px-4 py-2 placeholder-blue-500 md:rounded-r-md max-md:rounded-b-md" placeholder={user.name} disabled/>
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
                        <div className="flex flex-row max-md:flex-col">
                            <label className="w-30 font-lexend text-center font-bold text-white bg-blue-500 px-4 py-2 md:rounded-l-md max-md:rounded-t-md max-md:w-full">Apellido</label>
                            <input id="lastname" className="w-full font-lexend font-bold text-black-500 bg-white px-4 py-2 placeholder-blue-500 md:rounded-r-md max-md:rounded-b-md" placeholder={user.lastname} disabled/>
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
                        <div className="flex flex-row max-md:flex-col">
                            <label className="w-30 min-w-fit font-lexend text-center font-bold text-white bg-blue-500 px-4 py-2 md:rounded-l-md max-md:rounded-t-md max-md:w-full">Nombre de Usuario</label>
                            <div className="w-full font-lexend font-bold text-black-500 bg-white px-4 py-2 placeholder-blue-500 md:rounded-r-md max-md:rounded-b-md">{user.username}</div>
                        </div>
                        <div className="flex flex-row max-md:flex-col">
                            <label className="w-30 min-w-fit font-lexend text-center font-bold text-white bg-blue-500 px-4 py-2 md:rounded-l-md max-md:rounded-t-md max-md:w-full">Tipo de Usuario</label>
                            <div className="w-full font-lexend font-bold text-black-500 bg-white px-4 py-2 placeholder-blue-500 md:rounded-r-md max-md:rounded-b-md">{user.type}</div>
                        </div>
                        <div className="w-full flex flex-row justify-center">
                            <button className="w-40 px-4 py-2 bg-blue-500 font-lexend text-white font-bold transition-all duration-300 ease-in-out hover:bg-blue-800 rounded-full" onClick={() => {location.href = '/setPassword'}}>Cambiar Contraseña</button>
                        </div>
                    </section>
                }
            </div>
        </div>
    );
}