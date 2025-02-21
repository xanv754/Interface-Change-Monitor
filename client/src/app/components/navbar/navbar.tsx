import styles from '@styles/navbar.module.css';
import { UserInfoSchema } from '@/schemas/user';
import { Routes } from "@libs/routes";
import { ProfileTypes } from "@libs/types";
import { Token } from "@libs/token";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function Navbar() {
    const router = useRouter();
    const pathname = usePathname();
    const shortTitle = "MCI";
    const [user, setUser] = useState<UserInfoSchema | null>(null);

    const logout = () => {
        Token.clearToken();
        sessionStorage.clear();
        router.push(Routes.login);
    }

    const getUserInfo = () => {
        if (sessionStorage.getItem('user')) {
            const user = JSON.parse(sessionStorage.getItem('user') as string) as UserInfoSchema;
            if (user) setUser(user);
        }
    };

    useEffect(() => {
        console.log(pathname);
    }, [pathname]);

    useEffect(() => {
        getUserInfo();
        const elementTitle = document.getElementById('title');
        if ((elementTitle) && (elementTitle.scrollWidth > elementTitle.clientWidth)) {
            elementTitle.textContent = shortTitle;
        }

    }, []);

    return (
        <nav className='min-w-fit w-full bg-white-50 px-4 py-2 flex flex-col justify-between items-center rounded-full md:flex-row'>
            <div className='flex items-center gap-4'>
                <img src='/logo.png' alt='logo' width={40} />
                <h1 id="title" className='font-bold text-xl text-blue-950 text-nowrap whitespace-nowrap overflow-hidden text-ellipsis'>Monitoreo de Cambios de Interfaces</h1>
            </div>
            <div className='flex items-center gap-10 md:px-4'>
                {user && (user.profile === ProfileTypes.root || user.profile === ProfileTypes.soport) && 
                    <a href='#' className={`${pathname === Routes.home ? "text-gray-500" : "text-gray-300"} transition-all duration-300 ease-in-out hover:text-gray-500`}>Asignar</a>
                }
                {user && user.profile === ProfileTypes.standard && 
                    <a href='#' className={`${pathname === Routes.home ? "text-gray-500" : "text-gray-300"} transition-all duration-300 ease-in-out hover:text-gray-500`}>Asignaciones</a>
                }
                {user && user.profile === ProfileTypes.admin &&
                    <section className={`${styles.dropdown}`}>
                        <button className={`${((pathname === Routes.home) || (pathname === Routes.homeAssign)) ? "text-gray-500" : "text-gray-300"} transition-all duration-300 ease-in-out ${styles.dropbtn}`}>Asignaciones</button>
                        <div className={`${styles.dropdownContent}`}>
                            <a href="#" className='text-gray-300 text-sm rounde'>Mis Asignaciones</a>
                            <a href="#" className='text-gray-300 text-sm'>Asignar</a>
                        </div>
                    </section>
                }
                <section className={`${styles.dropdown}`}>
                    <button className={`${((pathname === Routes.historyGeneral) || (pathname === Routes.historyPersonal)) ? "text-gray-500" : "text-gray-300"} transition-all duration-300 ease-in-out ${styles.dropbtn}`}>Historial</button>
                    <div className={`${styles.dropdownContent}`}>
                        {user && (user.profile === ProfileTypes.root || user.profile === ProfileTypes.soport || user.profile === ProfileTypes.admin) &&
                            <a href="#" className='text-gray-300 text-sm rounde'>General</a>
                        }
                        {user && (user.profile === ProfileTypes.admin || user.profile === ProfileTypes.standard) &&
                            <a href="#" className='text-gray-300 text-sm'>Propio</a>
                        }
                    </div>
                </section>
                <section className={`${styles.dropdown}`}>
                    <button className={`${((pathname === Routes.statisticsGeneral) || (pathname === Routes.statisticsPersonal)) ? "text-gray-500" : "text-gray-300"} transition-all duration-300 ease-in-out ${styles.dropbtn}`}>Estadísticas</button>
                    <div className={`${styles.dropdownContent}`}>
                        {user && (user.profile === ProfileTypes.root || user.profile === ProfileTypes.soport || user.profile === ProfileTypes.admin) &&
                            <a href="#" className='text-gray-300 text-sm rounde'>General</a>
                        }
                        {user && (user.profile === ProfileTypes.admin || user.profile === ProfileTypes.standard) &&
                            <a href="#" className='text-gray-300 text-sm'>Propio</a>
                        }
                    </div>
                </section>
                <section className={`${styles.dropdown}`}>
                    <button className={`${pathname === Routes.profile ? "text-gray-500" : "text-gray-300"} transition-all duration-300 ease-in-out ${styles.dropbtn}`}>Cuenta</button>
                    <div className={`${styles.dropdownContent}`}>
                        <a href="#" className='text-gray-300 text-sm rounde'>Perfil</a>
                        <a onClick={logout} className='text-gray-300 text-sm'>Cerrar Sesión</a>
                    </div>
                </section>
            </div>
        </nav>
    );
}