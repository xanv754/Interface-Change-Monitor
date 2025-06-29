"use client";

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { PATHS } from '@/constants/paths';
import { RoleTypes } from '@/constants/types';
import { UserLoggedModel } from '@/model/users';
import { SessionController } from '@/controllers/session';


interface NavbarProps {
    user: UserLoggedModel | null;
}


export default function NavbarComponent(content: NavbarProps) {
    const router = useRouter();

    const handlerLogout = () => {
        SessionController.logout();
        router.push(PATHS.LOGIN);
    }

    useEffect(() => {
        if (content.user && !content.user.can_assign && !content.user.can_receive_assignment) {
            router.push(PATHS.LOBBY);
        }
    }, []);

    return (
        <nav className="w-full min-w-fit bg-(--blue) py-3 px-4 flex flex-col lg:flex-row justify-between">
            <h1 className='m-0 text-2xl font-bold text-(--white) mb-4 lg:mb-0'>Monitor de Cambios de Interfaces</h1>
            <ul className='m-0 p-0 flex flex-col md:flex-row gap-6 list-none items-center'>
                {content.user && content.user.can_assign &&
                    <li className="m-0"><a className="text-(--white) no-underline transition-all duration-300 ease-in-out hover:text-(--yellow)" href="/dashboard/admin">Inicio</a></li>
                }
                {content.user && !content.user.can_assign &&
                    <li className="m-0"><a className="text-(--white) no-underline transition-all duration-300 ease-in-out hover:text-(--yellow)" href="/dashboard/personal">Inicio</a></li>
                }
                {content.user && content.user.can_assign && content.user.can_receive_assignment &&
                    <li className="m-0"><a className="text-(--white) no-underline transition-all duration-300 ease-in-out hover:text-(--yellow)" href="/dashboard/personal">Mis Asignaciones</a></li>
                }
                {content.user && !content.user.can_assign && !content.user.can_receive_assignment &&
                    <li className="m-0"><a className="text-(--white) no-underline transition-all duration-300 ease-in-out hover:text-(--yellow)" href="/dashboard/personal">Mis Asignaciones</a></li>
                }
                {content.user && 
                    <li className="m-0"><a className="text-(--white) no-underline transition-all duration-300 ease-in-out hover:text-(--yellow)" href="/history/admin">Historial</a></li>
                }
                {content.user && content.user.view_information_global && 
                    <li className="m-0"><a className="text-(--white) no-underline transition-all duration-300 ease-in-out hover:text-(--yellow)" href="/statistics">Estadísticas</a></li>
                }
                {content.user && (content.user.role === RoleTypes.ROOT || content.user.role === RoleTypes.SOPORT) &&
                    <li className="m-0"><a className="text-(--white) deco" href="/settings">Configuración</a></li>
                }
                <li className="m-0"><a className="text-(--white) no-underline transition-all duration-300 ease-in-out hover:text-(--yellow)" href="/profile">Perfil</a></li>
                <li className="m-0"><a className="text-(--white) no-underline transition-all duration-300 ease-in-out hover:text-(--yellow)" onClick={handlerLogout}>Cerrar Sesión</a></li>
            </ul>
        </nav>
    );
}