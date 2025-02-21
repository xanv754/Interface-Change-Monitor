'use client';

import InputTextForm from '@components/form/input';
import { CurrentSession } from '@/libs/session';
import { SystemController } from '@/controllers/system';
import { UserController } from '@/controllers/user_';
import { Validate } from '@/libs/validate';
import { Routes } from '@/libs/routes';
import { useRouter } from "next/navigation";
import { useState, useEffect } from 'react';

export default function LoginView() {
    const router = useRouter();
    const [username, setUsername] = useState<string | null>(null);
    const [password, setPassword] = useState<string | null>(null);
    const [error, setError] = useState<boolean>(false);

    const handlerUsername = (username: string | null) => {
        setError(false);
        setUsername(username);
    };

    const handlerPassword = (password: string | null) => {
        setError(false);
        setPassword(password);
    };

    const redirect = () => {
        router.push(Routes.home);
    }

    const handleLogin = async (event: React.FormEvent) => {
        event.preventDefault();
        if (!username || !password) return;
        else {
            const credentials = await UserController.login(username, password);
            if (credentials) {
                await CurrentSession.saveInfo(credentials);
                redirect();
            } else setError(true);

        }
    };

    useEffect(() => {
        if (CurrentSession.getToken()) router.push(Routes.home);
    }, []);

    return (
        <main className="min-w-fit w-full h-full flex justify-center items-center">
            <form onSubmit={handleLogin} className="min-w-fit p-4 bg-white-50 rounded-lg flex flex-col justify-center items-center lg:w-1/3">
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
                    placeholder='Nombre de usuario'
                />
                <InputTextForm 
                    id="password" 
                    label="Contraseña" 
                    type="password" 
                    getInput={handlerPassword}
                    validateInput={Validate.validatePassword}
                    messageError="* Contraseña requerida"
                    placeholder='Contraseña'
                />
                <small className={`mb-1 ${error ? "block" : "hidden"} text-red-500 italic`}>Usuario o contraseña incorrectos</small>
                <button type="submit" className="bg-blue-800 text-white-50 font-bold px-10 py-2 rounded-full transition-all duration-300 ease-in-out hover:bg-blue-950">Iniciar Sesión</button>
            </form>
        </main>
    );
}