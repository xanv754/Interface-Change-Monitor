'use client';

import InputTextForm from '@/app/components/forms/input';
import AlertModal from '@app/components/modals/alert';
import LoadingModal from '@app/components/modals/loading';
import { UserService } from '@/services/user';
import { CurrentSession } from '@libs/session';
import { Validate } from '@libs/validate';
import { Routes } from '@libs/routes';
import { ProfileTypes } from '@libs/types';
import { UserShortInfoResponseSchema } from '@schemas/user';
import { useRouter } from "next/navigation";
import React, { useState, useEffect } from 'react';

export default function LoginView() {
    const router = useRouter();

    const [loading, setLoading] = useState<boolean>(true);
    const [errorCredentials, setErrorCredentials] = useState<boolean>(false);

    const [username, setUsername] = useState<string | null>(null);
    const [password, setPassword] = useState<string | null>(null);

    /**
     * Login to the system.
     * 
     * @param {React.FormEvent} event The event that was triggered by the user
     */
    const login = async (event: React.FormEvent) => {
        event.preventDefault();
        if (!username || !password) return;
        else {
            handlerLoading(true);
            const credentials = await UserService.login(username, password);
            if (credentials) {
                let user = await CurrentSession.saveInfo(credentials);
                handlerLoading(false);
                if (!user) handlerErrorCredentials(true);
                else redirectHome(user);
            } else handlerErrorCredentials(true);
        }
    };

    /**
     * Redirect to the home page of the user.
     * 
     * @param {UserShortInfoResponseSchema} user The user that was logged in.
     */
    const redirectHome = (user: UserShortInfoResponseSchema) => {
        if (user.profile === ProfileTypes.root || user.profile === ProfileTypes.soport) {
            router.push(Routes.homeAssign);
        } else if (user.profile === ProfileTypes.standard || user.profile === ProfileTypes.admin) {
            router.push(Routes.homeAssigned);
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
     * Handler for user error credentials status.
     * 
     * @param {boolean} isThereAnError If there is an error or not.
     */
    const handlerErrorCredentials = (isThereAnError: boolean = false) => {
        setErrorCredentials(isThereAnError);
    }

    /**
     * Handler to get username.
     * 
     * @param {string | null} username The user name that was entered by the user
     */
    const handlerUsername = (username: string | null) => {
        handlerErrorCredentials(false);
        setUsername(username);
    };

    /**
     * Handler to get password.
     * 
     * @param {string | null} password The password that was entered by the user
     */
    const handlerPassword = (password: string | null) => {
        handlerErrorCredentials(false);
        setPassword(password);
    };

    useEffect(() => {
        let user = CurrentSession.getInfoUser();
        if (user) redirectHome(user);
    }, []);

    return (
        <main className="min-w-fit w-full h-full flex justify-center items-center">
            <LoadingModal showModal={loading} />
            <form onSubmit={login} className="min-w-fit p-4 bg-white-50 rounded-lg flex flex-col justify-center items-center lg:w-1/3">
                <section className='w-full flex flex-col items-center gap-6 mb-4'>
                    <div className='w-fit flex flex-col items-center'>
                        <img src="/logo.png" alt="logo" width={80} />
                        <h1 className="w-80 font-bold text-3xl text-blue-950 text-wrap text-center md:w-96">
                            <span className='text-red-800'>M</span>onitoreo de <span className='text-red-800'>C</span>ambios de <span className='text-red-800'>I</span>nterfaces
                        </h1>
                    </div>
                    <div className='w-fit flex flex-col items-center'>
                        <h2 className='font-bold px-4 text-xl text-blue-950 lg:px-8'>Inicio de Sesión</h2>
                        <div className='w-full h-1 bg-blue-950 rounded-full'></div>
                    </div>
                </section>
                <InputTextForm 
                    id="username" 
                    label="Usuario" 
                    type="text" 
                    getInput={handlerUsername}
                    validateInput={Validate.validateUsername}
                    messageError="* Usuario válido requerido"
                    disabled={false}
                    placeholder='Nombre de usuario'
                />
                <InputTextForm 
                    id="password" 
                    label="Contraseña" 
                    type="password" 
                    getInput={handlerPassword}
                    validateInput={Validate.validatePassword}
                    disabled={false}
                    messageError="* Contraseña requerida"
                    placeholder='Contraseña'
                />
                <small className={`mb-1 ${errorCredentials ? "block" : "hidden"} text-red-500 italic`}>Usuario o contraseña incorrectos</small>
                <button type="submit" className="bg-blue-800 text-white-50 font-bold px-10 py-2 rounded-full transition-all duration-300 ease-in-out hover:bg-blue-950">Iniciar Sesión</button>
            </form>
        </main>
    );
}