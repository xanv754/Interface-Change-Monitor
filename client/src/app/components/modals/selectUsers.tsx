import { UserResponseSchema } from '@schemas/user';
import React, { useEffect, useState } from 'react';

interface SelectUserModalProps {
    showModal: boolean;
    users: UserResponseSchema[];
    acceptAction: (users: UserResponseSchema[]) => void;
    cancelAction: () => void;
}

export default function SelectUserModal(props: SelectUserModalProps) {
    const [usersSelected, setUsersSelected] = useState<UserResponseSchema[]>([]);

    const handlerAccept = () => {
        props.acceptAction(usersSelected);
    }

    const handlerCancel = () => {
        props.cancelAction();
    }

    const handlerCheck = (username: string) => {
        let statusAdd = true;
        let user = usersSelected.filter(user => user.username === username);
        if (user.length > 0) statusAdd = false;
        if (statusAdd) {
            let userSelected = props.users.filter(user => user.username === username);
            setUsersSelected([...usersSelected, userSelected[0]])
        } else {
            let usersWithUserSelected = usersSelected.filter(user => user.username !== username);
            setUsersSelected(usersWithUserSelected);
        }
    }

    useEffect(() => {
        const modalAccept = document.getElementById('modal-accept-users');
        const modalCancel = document.getElementById('modal-cancel-users');
        const modalState = document.getElementById('modal-state-users');

        if (modalAccept && modalCancel && modalState) {
            if (props.showModal) modalState.classList.remove('hidden');
            else modalState.classList.add('hidden');  
        }
    }, [props.showModal]);

    return(
        <div id="modal-state-users" className="absolute z-10" aria-labelledby="modal-title" role="dialog" aria-modal="true">
            <aside className="fixed inset-0 bg-gray-950 bg-opacity-55 transition-opacity" aria-hidden="true"></aside>
            <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
                <div id="modal-panel" className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
                    <div className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
                        <section className="bg-gray-50 px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                            <div className="sm:flex sm:items-start">
                                <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                                    <h3 className="text-base font-semibold leading-6 text-gray-900" id="modal-title">Usuarios a Asignar</h3>
                                    <div className="mt-2">
                                        <p className="text-sm text-gray-500">Seleccione los usuarios a quienes se les realizará la asignación automática</p>
                                    </div>
                                    <div className='w-full flex flex-col flex-wrap gap-1'>
                                        <h4 className='text-blue-800 font-bold text-sm'>Usuarios Disponibles:</h4>
                                        {props.users.length > 0 && 
                                            props.users.map((user: UserResponseSchema, index: number) => {
                                                return (
                                                    <div key={index} className='w-fit flex flex-row justify-center items-center gap-2'>
                                                        <label htmlFor={user.username} className='text-sm'>{user.name} {user.lastname}</label>
                                                        <input 
                                                            type="checkbox" 
                                                            onClick={() => {handlerCheck(user.username)}}
                                                            id={user.username} 
                                                            name={user.username} 
                                                            className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500" 
                                                        />
                                                    </div>
                                                );
                                            })
                                        }
                                    </div>
                                </div>
                            </div>
                        </section>
                        <section className="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                            <button 
                                id="modal-accept-users"
                                onClick={handlerAccept}
                                type="button" 
                                className="inline-flex w-full justify-center rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white-50 shadow-sm transition-all ease-linear duration-200 hover:bg-blue-700 sm:ml-3 sm:w-auto"
                            >
                                Aceptar
                            </button>
                            <button 
                                id="modal-cancel-users"
                                onClick={handlerCancel}
                                type="button" 
                                className="mt-3 inline-flex w-full justify-center rounded-md bg-white-50 px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 transition-all ease-linear duration-200 hover:bg-gray-500 hover:text-white-50 sm:mt-0 sm:w-auto"
                            >
                                Cancel
                            </button>
                        </section>
                    </div>
                </div>
            </div>
        </div>
    );
}