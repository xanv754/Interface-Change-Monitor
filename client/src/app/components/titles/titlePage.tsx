import { Routes } from '@libs/routes';
import { usePathname } from "next/navigation";
import { useState, useEffect } from "react";

export default function PageTitles() {
    const pathname = usePathname();
    const [title, setTitle] = useState<string>('');

    useEffect(() => {
        if (pathname === Routes.homeAssigned || pathname === Routes.homeAssign) {
            setTitle('Asignaciones');
        } else if (pathname === Routes.historyGeneral || pathname === Routes.historyPersonal) {
            setTitle('Historial');
        } else if (pathname === Routes.statisticsGeneral || pathname === Routes.statisticsPersonal) {
            setTitle('Estadísticas');
        } else if (pathname === Routes.profile) {
            setTitle('Perfil');
        }
    }, [pathname]);

    return (
        <div className='w-full flex flex-col items-center'>
            <div className='w-fit'>
                <h2 className='text-center text-3xl text-white-50 font-bold px-4'>{title}</h2>
                <div className='w-full h-1 mt-1 bg-yellow-500 rounded-full'></div>
            </div>
        </div>
    );
}