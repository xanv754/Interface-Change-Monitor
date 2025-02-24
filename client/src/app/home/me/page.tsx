'use client';

import { user_example } from "@app/example";
import Navbar from '@components/navbar/navbar';
import InputTextStateForm from '@components/form/inputState';
import InputTextForm from '@components/form/input';
import { Validate } from '@libs/validate';
import { Routes } from '@libs/routes';
import { UserSchema, UserUpdateSchema } from "@/schemas/user";
import { useState, useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";

export default function ProfileView() {
    const router = useRouter();
    const pathname = usePathname();
    const [user, setUser] = useState<UserSchema | null>(null);
    const [activeEditInfo, setActiveEditInfo] = useState<boolean>(true);
    const [activeEditPassword, setActiveEditPassword] = useState<boolean>(true);

    const [newName, setNewName] = useState<string | null>(null);
    const [newLastname, setNewLastname] = useState<string | null>(null);

    const handlerEditInfo = () => {
        setActiveEditInfo(!activeEditInfo);
    }

    const handlerEditPassword = () => {
        setActiveEditPassword(!activeEditPassword);
    }

    const handlerNewName = (newName: string | null) => {
        if (user) {
            if (newName && newName.length > 0) {
                setNewName(newName);
            } else {
                setNewName(user.name);
            }
        }
    }

    const handlerNewLastname = (newLastname: string | null) => {
        if (user) {
            if (newLastname && newLastname.length > 0) {
                setNewLastname(newLastname);
            } else {
                setNewLastname(user.lastname);
            }
        }
    }

    const updateInfoUser = async () => {
        if (user) {
            let currentName: string
            let currentLastname: string
            if (newName) currentName = newName;
            else currentName = user.name;
            if (newLastname) currentLastname = newLastname;
            else currentLastname = user.lastname;
            let newUser: UserUpdateSchema = {
                name: currentName,
                lastname: currentLastname,
            }
            console.log(newUser);
        }
    }

    const updatePasswordUser = async () => {
        console.log("Actualizando Contraseña...");
    }

    const getData = async () => {
        const data = await user_example;
        setUser(data);
        if (data) {
            setNewName(data.name);
            setNewLastname(data.lastname);
        } else {
            router.push(Routes.login);
        }
    };

    
    useEffect(() => {
        getData();
    }, []);

    return (
        <main className="w-full h-screen flex flex-col items-center">
            {user &&
                <>
                    <section className='w-full h-fit px-4 py-1 mb-4 flex flex-col gap-4'>
                        <Navbar />
                        {pathname === Routes.profile &&
                            <div className='w-full flex flex-col items-center'>
                                <div className='w-fit'>
                                    <h2 className='text-center text-3xl text-white-50 font-bold px-4'>Perfil</h2>
                                    <div className='w-full h-1 mt-1 bg-yellow-500 rounded-full'></div>
                                </div>
                            </div>
                        }
                    </section>
                    <section className='w-fit h-fit bg-gray-950 flex flex-col p-4 rounded-lg'>
                        <div className='w-full h-fit bg-gray-950 py-3 flex flex-col items-center justify-center gap-2 rounded-t-md'>
                            <h2 className='text-xl text-white-55 font-bold'>Información del Perfil</h2>
                            <div className='w-full h-fit flex justify-center items-center gap-2'>
                                {activeEditInfo && 
                                    <button 
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
                        <div className={`w-full h-fit bg-white-100 px-2 py-4 flex flex-col gap-3 items-center justify-start rounded-md lg:py-6`}>
                            <div className='w-full h-fit flex flex-row justify-center gap-3'>
                                <InputTextStateForm 
                                    id='name' 
                                    label='Nombre' 
                                    type='text'
                                    defaultValue={user.name}
                                    getInput={handlerNewName} 
                                    validateInput={Validate.validateName} 
                                    placeholder='Nuevo Nombre'
                                    disabled={activeEditInfo}
                                />
                                <InputTextStateForm 
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
                            <div className='w-full h-fit flex flex-row justify-center gap-3'>
                                <InputTextStateForm 
                                    id='profile' 
                                    label='Estatus del Perfil' 
                                    type='text'
                                    defaultValue={user.profile}
                                    getInput={() => {}} 
                                    validateInput={() => {return true}} 
                                    disabled={true}
                                />
                                <InputTextStateForm 
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
                        <div className='w-full bg-gray-950 py-3 h-fit mb-4 flex flex-col items-center justify-center gap-2'>
                            <h2 className='text-xl text-white-55 font-bold'>Actualizar Contraseña</h2>
                            <div className='w-full h-fit flex justify-center items-center gap-2'>
                                {activeEditPassword && 
                                    <button 
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
                        <div className='w-full h-fit px-2 py-4 bg-white-100 flex flex-row justify-center rounded-md gap-3'>
                                <InputTextForm 
                                    id='password' 
                                    label='Contraseña' 
                                    type='text'
                                    getInput={handlerNewName} 
                                    validateInput={Validate.validatePassword} 
                                    messageError='* Contraseña requerida'
                                    placeholder='Nueva contraseña'
                                    disabled={activeEditPassword}
                                />
                                <InputTextForm 
                                    id='confirmPassword' 
                                    label='Confirmar Contraseña' 
                                    type='text'
                                    getInput={handlerNewLastname} 
                                    validateInput={Validate.validatePassword} 
                                    messageError='* Contraseña requerida'
                                    placeholder='Confirmar nueva contraseña'
                                    disabled={activeEditPassword}
                                />
                        </div>
                    </section>
                </>
            }
        </main>
    );
}