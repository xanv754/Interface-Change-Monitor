'use client';

import { use, useEffect } from "react";

export interface InputCalendarProps {
    id: string;
    label: string;
    getValue: (value: string) => void;
    disabled: boolean;
}

export default function InputCalendarForm(props: InputCalendarProps) {
    const today = new Date();
    const month = today.getMonth();

    const handlerValue = (event: React.ChangeEvent<HTMLInputElement>) => {
        let value = event.target.value;
        props.getValue(value);
    };

    useEffect(() => {
        console.log(props.disabled);
    }, []);
    
    return (
        <div className='w-fit flex flex-col lg:flex-row'>
            <label htmlFor={props.id} className='min-w-fit bg-blue-800 px-2 py-1 text-white-50 rounded-t-xl lg:rounded-l-xl lg:rounded-tr-none'>{props.label}</label>
            <input 
                id={props.id} 
                onChange={handlerValue} 
                className={`min-w-fit bg-white-100 ${props.disabled ? "bg-gray-400 cursor-not-allowed" : "bg-white-100"} px-4 py-1 appearance-none border-1 border-blue-950 rounded-b-xl lg:rounded-r-xl lg:lg:rounded-bl-none`}
                type="month"
                min={month}
                disabled={props.disabled}
            />
        </div>
    );
}