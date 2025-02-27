'use client';

import { AssignmentInfoResponseSchema } from '@/schemas/assignment';
import { useEffect, useState } from "react";

export interface InterfaceAssignedCardProps {
    data: AssignmentInfoResponseSchema;
    handlerData: (change: AssignmentInfoResponseSchema, status: boolean) => void;
}

export default function InterfaceAssignedCard(props: InterfaceAssignedCardProps) {
    const [checked, setChecked] = useState<boolean>(false);

    useEffect(() => {
        if (checked) {
            props.handlerData(props.data, true);
        } else {
            props.handlerData(props.data, false);
        }
    }, [checked]);

    return (
        <div className='w-full bg-white-55 flex flex-col items-center justify-center rounded-lg mb-2 shadow-md drop-shadow-[1px_1px_2px_rgba(0,0,0,0.25)]'>
            <section className='w-full px-4 py-2 bg-white-50 flex flex-row items-center rounded-t-lg'>
                <section className='w-full flex flex-row flex-wrap items-center gap-2 md:gap-8'>
                    <div id="ip" className='w-fit flex flex-row gap-2 items-center justify-start'>
                        <h3 className='text-lg text-blue-800 font-bold self-center'>IP:</h3>
                        <p className='text-gray-700 font-semibold'>{props.data.ip}</p>
                    </div>
                    <div id="community" className='w-fit max-w-72 flex flex-row gap-2 items-center justify-start'>
                        <h3 className='text-lg text-blue-800 font-bold self-center'>Community:</h3>
                        <p className='text-gray-700 font-semibold overflow-hidden text-ellipsis whitespace-nowrap'>{props.data.community}</p>
                    </div>
                    <div id="sysname" className='w-fit max-w-72 flex flex-row gap-2 items-center justify-start'>
                        <h3 className='text-lg text-blue-800 font-bold self-center'>Sysname:</h3>
                        <p className='text-gray-700 font-semibold overflow-hidden text-ellipsis whitespace-nowrap'>{props.data.sysname}</p>
                    </div>
                    <div id="ifIndex" className='w-fit max-w-72 flex flex-row gap-2 items-center justify-start'>
                        <h3 className='text-lg text-blue-800 font-bold self-center'>ifIndex:</h3>
                        <p className='text-gray-700 font-semibold overflow-hidden text-ellipsis whitespace-nowrap'>{props.data.ifIndex}</p>
                    </div>
                </section>
                <div className='w-fit flex justify-center items-center'>
                    <input 
                        type="checkbox" 
                        checked={checked} 
                        onChange={() => setChecked(!checked)} 
                        className={`w-8 h-6 rounded-md ${checked ? "bg-blue-950" : "bg-white-50"} cursor-pointer`}
                    />
                    <span className={`absolute ${checked ? "bg-blue-950" : "bg-white-50"} cursor-pointer ring-1 ring-inset ring-blue-950`} onClick={() => setChecked(!checked)} >
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="white" d="m9.55 18l-5.7-5.7l1.425-1.425L9.55 15.15l9.175-9.175L20.15 7.4z"/></svg>
                    </span>
                </div>
            </section>
            <section className='w-full px-4 flex flex-col gap-1 md:flex-row md:gap-5'>
                <h4 className='text-sm text-gray-700 font-bold'>Fecha de Asignación: {props.data.dateAssignment}</h4>
                <h4 className='text-sm text-gray-700 font-bold'>Asignado por: {props.data.assignedBy}</h4>
            </section>
            <section className='w-full px-4 py-1 flex flex-col gap-4 md:flex-row'>
                <section id='data-old-interface' className='w-1/2 flex flex-col'>
                    <h3 className='text-gray-700 mb-1 font-bold'>Datos de la Interfaz Viejos</h3>
                    <div id="ifName" className='w-fit flex flex-col items-start md:flex-row md:items-center md:justify-start md:gap-2'>
                        <h3 className='text-sm text-blue-800 font-bold self-center'>Nombre - ifName:</h3>
                        <p className='text-sm text-gray-700 font-semibold'>{props.data.oldIfName}</p>
                    </div>
                    <div id="ifDescr" className='w-fit flex flex-col items-start md:flex-row md:items-center md:justify-start md:gap-2'>
                        <h3 className='text-sm text-blue-800 font-bold self-center'>Descripción - ifDescr:</h3>
                        <p className='text-sm text-gray-700 font-semibold'>{props.data.oldIfDescr}</p>
                    </div>
                    <div id="ifAlias" className='w-fit flex flex-col items-start md:flex-row md:items-center md:justify-start md:gap-2'>
                        <h3 className='text-sm text-blue-800 font-bold self-center'>Alias - ifAlias:</h3>
                        <p className='text-sm text-gray-700 font-semibold'>{props.data.oldIfAlias}</p>
                    </div>
                    <div id="ifHighSpeed" className='w-fit flex flex-col items-start md:flex-row md:items-center md:justify-start md:gap-2'>
                        <h3 className='text-sm text-blue-800 font-bold self-center'>Capacidad - ifHighSpeed:</h3>
                        <p className='text-sm text-gray-700 font-semibold'>{props.data.oldIfHighSpeed}</p>
                    </div>
                    <div id="ifOperStatus" className='w-fit flex flex-col items-start md:flex-row md:items-center md:justify-start md:gap-2'>
                        <h3 className='text-sm text-blue-800 font-bold self-center'>Estatus Operativo - ifOperStatus:</h3>
                        <p className='text-sm text-gray-700 font-semibold'>{props.data.oldIfOperStatus}</p>
                    </div>
                    <div id="ifAdminStatus" className='w-fit flex flex-col items-start md:flex-row md:items-center md:justify-start md:gap-2'>
                        <h3 className='text-sm text-blue-800 font-bold self-center'>Estatus Administrativo - ifAdminStatus:</h3>
                        <p className='text-sm text-gray-700 font-semibold'>{props.data.oldIfAdminStatus}</p>
                    </div>
                </section>
                <section id='data-new-interface' className='w-fit flex flex-col'>
                    <h3 className='text-gray-700 mb-1 font-bold'>Datos de la Interfaz Nuevos</h3>
                    <div id="ifName" className='w-fit flex flex-col items-start md:flex-row md:items-center md:justify-start md:gap-2'>
                        <h3 className='text-sm text-blue-800 font-bold'>Nombre - ifName:</h3>
                        <p className='text-sm text-wrap text-gray-700 font-semibold'>{props.data.newIfName}</p>
                    </div>
                    <div id="ifDescr" className='w-fit flex flex-col items-start md:flex-row md:items-center md:justify-start md:gap-2'>
                        <h3 className='text-sm text-blue-800 font-bold self-center'>Descripción - ifDescr:</h3>
                        <p className='text-sm text-gray-700 font-semibold'>{props.data.newIfDescr}</p>
                    </div>
                    <div id="ifAlias" className='w-fit flex flex-col items-start md:flex-row md:items-center md:justify-start md:gap-2'>
                        <h3 className='text-sm text-blue-800 font-bold self-center'>Alias - ifAlias:</h3>
                        <p className='text-sm text-gray-700 font-semibold'>{props.data.newIfAlias}</p>
                    </div>
                    <div id="ifHighSpeed" className='w-fit flex flex-col items-start md:flex-row md:items-center md:justify-start md:gap-2'>
                        <h3 className='text-sm text-blue-800 font-bold self-center'>Capacidad - ifHighSpeed:</h3>
                        <p className='text-sm text-gray-700 font-semibold'>{props.data.newIfHighSpeed}</p>
                    </div>
                    <div id="ifOperStatus" className='w-fit flex flex-col items-start md:flex-row md:items-center md:justify-start md:gap-2'>
                        <h3 className='text-sm text-blue-800 font-bold self-center'>Estatus Operativo - ifOperStatus:</h3>
                        <p className='text-sm text-gray-700 font-semibold'>{props.data.newIfOperStatus}</p>
                    </div>
                    <div id="ifAdminStatus" className='w-fit flex flex-col items-start md:flex-row md:items-center md:justify-start md:gap-2'>
                        <h3 className='text-sm text-blue-800 font-bold self-center'>Estatus Administrativo - ifAdminStatus:</h3>
                        <p className='text-sm text-gray-700 font-semibold'>{props.data.newIfAdminStatus}</p>
                    </div>
                </section>
            </section>
        </div>
    );
}