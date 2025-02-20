'use client';

import InputTextForm from '@components/form/input';
import { Token } from '@utils/token';
import { UserController } from '@/controllers/user';
import { Validate } from '@/libs/validate';
import { useRouter } from "next/navigation";
import { useState, useEffect } from 'react';

export default function LoginView() {
    const router = useRouter();
    const [username, setUsername] = useState<string | null>(null);
    const [password, setPassword] = useState<string | null>(null);

    const handlerUsername = (username: string) => {
        setUsername(username);
    };

    const handlerPassword = (password: string) => {
        setPassword(password);
    };

    const handleLogin = async () => {
        if (!username || !password) return;
        const credentials = await UserController.login(username, password);
        if (credentials) Token.setToken(credentials.access_token);
        router.push("/home");
    };

    useEffect(() => {
        if (Token.getToken()) router.push("/home");
        else sessionStorage.clear();
    }, []);

    return (
        <main className="min-w-fit w-full h-full flex justify-center items-center">
            <form action={handleLogin} className="w-fit max-w-96 p-4 bg-white-50 rounded-lg flex flex-col justify-center items-center">
                <h1 className="font-bold italic text-2xl text-blue-800 mb-5 text-wrap text-center">Control de Monitoreo de Interfaces</h1>
                <InputTextForm 
                    id="username" 
                    label="Usuario" 
                    type="text" 
                    getInput={handlerUsername}
                    validateInput={Validate.validateUsername}
                    messageError="* Usuario válido requerido"
                />
                <InputTextForm 
                    id="password" 
                    label="Contraseña" 
                    type="password" 
                    getInput={handlerPassword}
                    validateInput={Validate.validatePassword}
                    messageError="* Contraseña requerida"
                />
                <button type="submit" className="bg-blue-800 text-white-50 font-bold px-10 py-2 rounded-full transition-all duration-300 ease-in-out hover:bg-blue-950">Iniciar Sesión</button>
            </form>
        </main>
    );
}