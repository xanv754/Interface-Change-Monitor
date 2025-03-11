'use client';

import Navbar from '@components/navbar/navbar';
import InputTextWithDefaultValueForm from '@app/components/forms/inputState';
import LoadingModal from '@app/components/modals/loading';
import PageTitles from '@app/components/titles/titlePage';
import AlertModal from "@app/components/modals/alert";
import { CurrentSession } from "@/libs/session";
import { Validate } from '@libs/validate';
import { UserService } from "@/services/user";
import { UserLogginResponseSchema, UserUpdateInfoRequestSchema, UserUpdatePasswordRequestSchema } from "@schemas/user";
import { useState, useEffect } from "react";

export default function ProfileView() {
    const [loading, setLoading] = useState<boolean>(true);
    const [errorInfo, setErrorInfo] = useState<boolean>(false);
    const [errorUpdateInfo, setErrorUpdateInfo] = useState<boolean>(false);
    const [errorUpdatePassword, setErrorUpdatePassword] = useState<boolean>(false);
    const [errorEqualPassword, setErrorEqualPassword] = useState<boolean>(false);
    const [successUpdate, setSuccessUpdate] = useState<boolean>(false);

    const [token, setToken] = useState<string | null>(null);
    const [user, setUser] = useState<UserLogginResponseSchema | null>(null);

    const [activeEditInfo, setActiveEditInfo] = useState<boolean>(true);
    const [activeEditPassword, setActiveEditPassword] = useState<boolean>(true);
    const [newName, setNewName] = useState<string | null>(null);
    const [newLastname, setNewLastname] = useState<string | null>(null);
    const [newPassword, setNewPassword] = useState<string | null>(null);
    const [confirmPassword, setConfirmPassword] = useState<string | null>(null);

    /**
     * Get the information of the user logged in and your pending assignments.
     */
    const getData = async () => {
        let currentToken = CurrentSession.getToken();
        if (currentToken) {
            setToken(currentToken);
            const data = await UserService.getInfoUser(currentToken);
            if (data) {
                setUser(data);
                handlerLoading(false);
            }
            else {
                handlerLoading(false);
                handlerErrorInfo(true);
            }
        }
        else {
            handlerLoading(false);
            handlerErrorInfo(true);
        }
    };

    /**
     * Update the information of the user.
     */
    const updateInfoUser = async () => {
        if (token && user) {
            handlerLoading(true);
            let currentName: string
            let currentLastname: string
            if (newName) currentName = newName;
            else currentName = user.name;
            if (newLastname) currentLastname = newLastname;
            else currentLastname = user.lastname;
            let newUser: UserUpdateInfoRequestSchema = {
                name: currentName,
                lastname: currentLastname,
            }
            let statusUpdate = await UserService.updateInfo(token, newUser);
            if (statusUpdate) {
                setSuccessUpdate(true);
                setActiveEditInfo(true);
                setActiveEditPassword(true);
                handlerLoading(false);
            }
            else {
                handlerLoading(false);
                setErrorUpdateInfo(true);
            }
        } else {
            handlerLoading(false);
            handlerErrorInfo(true);
        }
    }

    /**
     * Update password user
     */
    const updatePasswordUser = async () => {
        handlerErrorEqualPassword();
        if (token && newPassword && confirmPassword) {
            if (newPassword === confirmPassword) {
                handlerLoading(true);
                let currentPassword: UserUpdatePasswordRequestSchema = {
                    password: newPassword
                }
                const status = await UserService.updatePassword(token, currentPassword);
                if (status) {
                    setSuccessUpdate(true);
                    setActiveEditInfo(true);
                    setActiveEditPassword(true);
                    handlerLoading(false);
                }
                else {
                    handlerLoading(false);
                    setErrorUpdatePassword(true);
                }
            } else handlerErrorEqualPassword(true);
        } else if (!token) {
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
     * Handler for user error info.
     * 
     * @param {boolean} isThereAnError If there is an error or not.
     */
    const handlerErrorInfo = (isThereAnError: boolean = false) => {
        setErrorInfo(isThereAnError);
    }

    /**
     * Handler for user error update status.
     * 
     * @param {boolean} isThereAnError If there is an error or not.
     */
    const handlerErrorUpdate = (isThereAnError: boolean = false) => {
        setErrorUpdateInfo(isThereAnError);
    }

    /**
     * Handler for user error update status of password.
     * 
     * @param {boolean} isThereAnError If there is an error or not.
     */
    const handlerErrorPassword = (isThereAnError: boolean = false) => {
        setErrorUpdatePassword(isThereAnError);
    }


    /**
     * Handler for user error equal password status.
     * 
     * @param {boolean} isThereAnError If there is an error or not.
     */
    const handlerErrorEqualPassword = (isThereAnError: boolean = false) => {
        setErrorEqualPassword(isThereAnError);
    }

    /**
     * Handler for success update status of assignments.
     * 
     * @param isSuccess 
     */
    const handlerSuccessUpdate = (isSuccess: boolean = false) => {
        setSuccessUpdate(isSuccess);
    }

    /**
     * Handler to activate the edit section of the user's information.
     */
    const handlerEditInfo = () => {
        setActiveEditInfo(!activeEditInfo);
    }

    /**
     * Handler to activate the edit section of the user's password.
     */
    const handlerEditPassword = () => {
        setActiveEditPassword(!activeEditPassword);
    }

    /**
     * Handler to get the new name of the user.
     * 
     * @param {string | null} newName The new name of the user.
     */
    const handlerNewName = (newName: string | null) => {
        if (user) {
            if (newName && newName.length > 0) {
                setNewName(newName);
            } else {
                setNewName(user.name);
            }
        }
    }

    /**
     * Handler to get the new lastname of the user.
     * 
     * @param {string | null} newLastname The new lastname of the user.
     */
    const handlerNewLastname = (newLastname: string | null) => {
        if (user) {
            if (newLastname && newLastname.length > 0) {
                setNewLastname(newLastname);
            } else {
                setNewLastname(user.lastname);
            }
        }
    }

    /**
     * Handler to get the new password of the user.
     * 
     * @param {string | null} newPassword The new password of the user.
     */
    const handlerNewPassword = (newPassword: string | null) => {
        setNewPassword(newPassword);
    }

    /**
     * Handler to get the confirm password of the user.
     * 
     * @param {string | null} confirmPassword The confirm password of the user.
     */
    const handlerConfirmPassword = (confirmPassword: string | null) => {
        setConfirmPassword(confirmPassword);
    }

    useEffect(() => {
        handlerErrorEqualPassword(false);
    }, [newPassword, confirmPassword]);

    useEffect(() => {
        getData();
    }, []);

    return (
        <main className="w-full h-screen flex flex-col items-center">
            <LoadingModal showModal={loading} />
            {errorInfo && 
                <AlertModal 
                    showModal={true} 
                    title="Error al obtener la información" 
                    message="Ocurrió un error al obtener la información. Por favor, refresca la página e inténtelo de nuevo. Si el error persiste, consulte a soporte." 
                    afterAction={handlerErrorInfo}
                />
            }
            {errorUpdateInfo && 
                <AlertModal 
                    showModal={true} 
                    title="Actualización de Usuario Fallida" 
                    message="Ocurrió un error al intentar actualizar el usuario. Por favor, refresca la página e inténtelo de nuevo. Si el error persiste, consulte a soporte." 
                    afterAction={handlerErrorUpdate}
                />
            }
            {errorUpdatePassword && 
                <AlertModal 
                    showModal={true} 
                    title="Actualización de Contraseña Fallida" 
                    message="Ocurrió un error al intentar actualizar la contraseña. Por favor, refresca la página e inténtelo de nuevo. Si el error persiste, consulte a soporte." 
                    afterAction={handlerErrorPassword}
                />
            }
            {successUpdate && 
                <AlertModal 
                    showModal={true} 
                    title="Actualización de Usuario Exitosa" 
                    message="El usuario ha sido actualizado con éxito. Refresca la página para ver los cambios."
                    afterAction={handlerSuccessUpdate}
                />
            }
            {user && <>
                <section id='header' className='w-full h-fit px-4 py-1 mb-4 flex flex-col gap-4'>
                    <Navbar />
                    <PageTitles />
                </section>
                <section id='container' className='w-fit h-fit bg-gray-950 flex flex-col p-4 rounded-lg'>
                    <div id='user-edit-header' className='w-full h-fit bg-gray-950 py-3 flex flex-col items-center justify-center gap-2 rounded-t-md'>
                        <h2 id='title-user-edit' className='text-xl text-white-55 font-bold'>Información del Perfil</h2>
                        <div id='buttons-options-user-edit' className='w-full h-fit flex justify-center items-center gap-2'>
                            {activeEditInfo && 
                                <button
                                    id='activate-user-edit'
                                    onClick={handlerEditInfo}
                                    className={`px-4 py-1 bg-blue-800 rounded-full text-white-50 transition-all duration-300 ease-in-out hover:bg-green-800`}>
                                        Actualizar Datos
                                </button>
                            }
                            {!activeEditInfo && 
                                <div className='w-full h-fit flex justify-center items-center gap-2'>
                                    <button
                                        id='cancel-edit'
                                        onClick={handlerEditInfo}
                                        className={`px-4 py-1 bg-blue-800 rounded-full text-white-50 transition-all duration-300 ease-in-out hover:bg-red-700`}>
                                            Cancelar
                                    </button>
                                    <button 
                                        id='update-edit'
                                        onClick={updateInfoUser}
                                        className={`px-4 py-1 bg-blue-800 rounded-full text-white-50 transition-all duration-300 ease-in-out hover:bg-green-800`}>
                                            Guardar
                                    </button>
                                </div>
                            }
                        </div>
                    </div>
                    <div id='user-edit' className='w-full h-fit bg-white-100 px-2 py-4 flex flex-col gap-3 items-center justify-start rounded-md lg:py-6'>
                        <div id='info-username' className='w-full h-fit flex flex-row justify-center gap-3'>
                            <InputTextWithDefaultValueForm 
                                id='username' 
                                label='Nombre de Usuario' 
                                type='text'
                                defaultValue={user.username}
                                getInput={() => {}} 
                                validateInput={() => {return true}} 
                                disabled={true}
                            />
                        </div>
                        <div id='update-names' className='w-full h-fit flex flex-row justify-center gap-3'>
                            <InputTextWithDefaultValueForm 
                                id='name' 
                                label='Nombre' 
                                type='text'
                                defaultValue={user.name}
                                getInput={handlerNewName} 
                                validateInput={Validate.validateName} 
                                placeholder='Nuevo Nombre'
                                disabled={activeEditInfo}
                            />
                            <InputTextWithDefaultValueForm 
                                id='lastname' 
                                label='Apellido' 
                                type='text'
                                defaultValue={user.lastname}
                                getInput={handlerNewLastname} 
                                validateInput={Validate.validateName} 
                                placeholder='Nuevo Apellido'
                                disabled={activeEditInfo}
                            />
                        </div>
                        <div id='info' className='w-full h-fit flex flex-row justify-center gap-3'>
                            <InputTextWithDefaultValueForm 
                                id='profile' 
                                label='Estatus del Perfil' 
                                type='text'
                                defaultValue={user.profile}
                                getInput={() => {}} 
                                validateInput={() => {return true}} 
                                disabled={true}
                            />
                            <InputTextWithDefaultValueForm 
                                id='account' 
                                label='Estatus de la Cuenta' 
                                type='text'
                                defaultValue={user.account}
                                getInput={() => {}} 
                                validateInput={() => {return true}} 
                                disabled={true}
                            />
                        </div>
                    </div>
                    <div id='password-edit' className='w-full bg-gray-950 py-3 h-fit mb-4 flex flex-col items-center justify-center gap-2'>
                        <h2 id='title-password-edit' className='text-xl text-white-55 font-bold'>Actualizar Contraseña</h2>
                        <div id='buttons-options-password-edit' className='w-full h-fit flex justify-center items-center gap-2'>
                            {activeEditPassword && 
                                <button 
                                    id='activate-edit-password'
                                    onClick={handlerEditPassword}
                                    className={`px-4 py-1 bg-blue-800 rounded-full text-white-50 transition-all duration-300 ease-in-out hover:bg-green-800`}>
                                        Actualizar Contraseña
                                </button>
                            }
                            {!activeEditPassword && 
                                <div className='w-full h-fit flex justify-center items-center gap-2'>
                                    <button 
                                        id='cancel-edit'
                                        onClick={handlerEditPassword}
                                        className={`px-4 py-1 bg-blue-800 rounded-full text-white-50 transition-all duration-300 ease-in-out hover:bg-red-700`}>
                                            Cancelar
                                    </button>
                                    <button 
                                        id='update-edit'
                                        onClick={updatePasswordUser}
                                        className={`px-4 py-1 bg-blue-800 rounded-full text-white-50 transition-all duration-300 ease-in-out hover:bg-green-800`}>
                                            Guardar
                                    </button>
                                </div>
                            }
                        </div>
                    </div>
                    <div id='password-edit' className='w-full h-fit px-2 py-4 bg-white-100 flex flex-col items-center justify-center rounded-md'>
                        <div id='form-password' className='w-full h-fit flex flex-row justify-center gap-3'>
                            <InputTextWithDefaultValueForm 
                                id='password' 
                                label='Contraseña' 
                                type='text'
                                defaultValue='******'
                                getInput={handlerNewPassword} 
                                validateInput={Validate.validatePassword} 
                                disabled={activeEditPassword}
                            />
                            <InputTextWithDefaultValueForm 
                                id='password-confirm' 
                                label='Confirmar Contraseña' 
                                type='text'
                                defaultValue='******'
                                getInput={handlerConfirmPassword} 
                                validateInput={Validate.validatePassword} 
                                disabled={activeEditPassword}
                            />
                        </div>
                        <small className={`text-red-500 ${errorEqualPassword && !activeEditPassword ? 'visible' : 'hidden'}`}>* Las contraseñas deben coincidir</small>
                    </div>
                </section>
            </>}
        </main>
    );
}