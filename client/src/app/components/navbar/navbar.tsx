import styles from '@styles/navbar.module.css';
import { CurrentSession } from '@/libs/session';
import { ProfileTypes } from "@libs/types";
import { Routes } from "@libs/routes";
import { UserShortInfoResponseSchema } from '@schemas/user';
import { ConfigurationResponseSchema } from '@schemas/configuration';
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function Navbar() {
    const router = useRouter();
    const pathname = usePathname();
    const shortTitle = "MCI";
    const [user, setUser] = useState<UserShortInfoResponseSchema | null>(null);
    const [config, setConfig] = useState<ConfigurationResponseSchema | null>(null);

    const logout = () => {
        CurrentSession.deleteSession();
        router.push(Routes.login);
    }

    useEffect(() => {
        const currentUser = CurrentSession.getInfoUser();
        if (currentUser) setUser(currentUser);

        const currentConfig = CurrentSession.getInfoConfig();
        if (currentConfig) setConfig(currentConfig);

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
                {user && config &&
                    <section className={`${styles.dropdown}`}>
                        <button className={`${((pathname === Routes.homeAssigned) || (pathname === Routes.homeAssign)) ? "text-gray-500" : "text-gray-300"} transition-all duration-300 ease-in-out ${styles.dropbtn}`}>Asignaciones</button>
                        <div className={`${styles.dropdownContent}`}>
                            {((config.canAssign.ROOT && user.profile === ProfileTypes.root) || 
                              (config.canAssign.SOPORT && user.profile === ProfileTypes.soport) ||
                              (config.canAssign.ADMIN && user.profile === ProfileTypes.admin) ||
                              (config.canAssign.STANDARD && user.profile === ProfileTypes.standard)
                             ) && 
                                <a href={`${Routes.homeAssign}`} className='text-gray-300 text-sm'>Asignar</a>
                            }
                            {((config.canReceiveAssignment.ROOT && user.profile === ProfileTypes.root) || 
                              (config.canReceiveAssignment.SOPORT && user.profile === ProfileTypes.soport) ||
                              (config.canReceiveAssignment.ADMIN && user.profile === ProfileTypes.admin) ||
                              (config.canReceiveAssignment.STANDARD && user.profile === ProfileTypes.standard)
                             ) && 
                                <a href={`${Routes.homeAssigned}`} className='text-gray-300 text-sm rounde'>Mis Asignaciones</a>
                            }
                        </div>
                    </section>
                }
                {user && config &&
                    <section className={`${styles.dropdown}`}>
                        <button className={`${((pathname === Routes.historyGeneral) || (pathname === Routes.historyPersonal)) ? "text-gray-500" : "text-gray-300"} transition-all duration-300 ease-in-out ${styles.dropbtn}`}>Historial</button>
                        <div className={`${styles.dropdownContent}`}>
                            {((config.viewAllStatistics.ROOT && user.profile === ProfileTypes.root) || 
                              (config.viewAllStatistics.SOPORT && user.profile === ProfileTypes.soport) ||
                              (config.viewAllStatistics.ADMIN && user.profile === ProfileTypes.admin) ||
                              (config.viewAllStatistics.STANDARD && user.profile === ProfileTypes.standard)
                             ) && 
                                <a href={`${Routes.historyGeneral}`} className='text-gray-300 text-sm rounde'>General</a>
                            }
                            {((config.canReceiveAssignment.ADMIN && user.profile === ProfileTypes.admin) ||
                              (config.canReceiveAssignment.STANDARD && user.profile === ProfileTypes.standard)
                             ) && 
                                <a href={`${Routes.historyPersonal}`} className='text-gray-300 text-sm'>Propio</a>
                            }
                        </div>
                    </section>
                }
                {user && config &&
                    <section className={`${styles.dropdown}`}>
                        <button className={`${((pathname === Routes.statisticsGeneral) || (pathname === Routes.statisticsPersonal)) ? "text-gray-500" : "text-gray-300"} transition-all duration-300 ease-in-out ${styles.dropbtn}`}>Estadísticas</button>
                        <div className={`${styles.dropdownContent}`}>
                            {((config.viewAllStatistics.ROOT && user.profile === ProfileTypes.root) || 
                              (config.viewAllStatistics.SOPORT && user.profile === ProfileTypes.soport) ||
                              (config.viewAllStatistics.ADMIN && user.profile === ProfileTypes.admin) ||
                              (config.viewAllStatistics.STANDARD && user.profile === ProfileTypes.standard)
                             ) && 
                                <a href={`${Routes.statisticsGeneral}`} className='text-gray-300 text-sm rounde'>General</a>
                            }
                            {((config.canReceiveAssignment.ADMIN && user.profile === ProfileTypes.admin) ||
                              (config.canReceiveAssignment.STANDARD && user.profile === ProfileTypes.standard)
                             ) && 
                                <a href={`${Routes.statisticsPersonal}`} className='text-gray-300 text-sm'>Propio</a>
                            }
                        </div>
                    </section>
                }
                <section className={`${styles.dropdown}`}>
                    <button className={`${pathname === Routes.profile ? "text-gray-500" : "text-gray-300"} transition-all duration-300 ease-in-out ${styles.dropbtn}`}>Cuenta</button>
                    <div className={`${styles.dropdownContent}`}>
                        <a href={`${Routes.profile}`} className='text-gray-300 text-sm rounde'>Perfil</a>
                        <a onClick={logout} className='text-gray-300 text-sm cursor-pointer'>Cerrar Sesión</a>
                    </div>
                </section>
            </div>
        </nav>
    );
}