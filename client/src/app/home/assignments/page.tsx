'use client';

import Navbar from '@components/navbar/navbar';
import { UserController } from "@/controllers/user";
import { UserInfoSchema } from "@schemas/user";
import { Routes } from '@/libs/routes';
import { Token } from "@utils/token";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

export default function HomeView() {
    const pathname = usePathname();
    const [user, setUser] = useState<UserInfoSchema | null>(null);

    const getUser = async () => {
        if (sessionStorage.getItem('user')) {
            const user = JSON.parse(sessionStorage.getItem('user') as string) as UserInfoSchema;
            if (user) setUser(user);
        }
    };
    
    useEffect(() => {
        getUser();
    }, []);

    return (
        <main className="w-full h-screen flex flex-col">
            <section className='w-full h-fit px-4 py-1 mb-4 flex flex-col gap-4'>
                <Navbar />
                {user && 
                    <h1 className='text-3xl text-white-50 font-bold px-2 md:px-8'>¡Bienvenido, <span className='italic'>{user.name} {user.lastname}!</span></h1>
                }
                {pathname === Routes.home &&
                    <div className='w-full flex flex-col items-center'>
                        <div className='w-fit'>
                            <h2 className='text-center text-2xl text-white-50 font-bold px-4'>Asignaciones</h2>
                            <div className='w-full h-1 mt-1 bg-yellow-500 rounded-full'></div>
                        </div>
                    </div>
                }
            </section>
            <section className='h-full bg-gray-950 px-4 py-2'>
                <p className='text-white-50 italic font-bold'>Aquí va el contenido</p>
            </section>
        </main>
    );
}