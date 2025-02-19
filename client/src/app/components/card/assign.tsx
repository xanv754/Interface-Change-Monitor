import SelectorOperatorForm from '../form/selectOperator';
import { ChangeSchema } from '@/schemas/changes';
import { OperatorSchema } from '@/schemas/operator';

export interface InterfaceAssignCardProps {
    data: ChangeSchema;
    operators: OperatorSchema[];
}

export default function InterfaceAssignCard(props: InterfaceAssignCardProps) {
    return (
        <div className='w-80 bg-white-50 p-4 flex flex-col items-center justify-center rounded-md'>
            <SelectorOperatorForm id='assingOperator' label='Asignar a' options={props.operators} />
            <section className='min-w-fit flex flex-col gap-0.5 self-start'>
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
                    <p className='text-gray-700 font-semibold overflow-hidden text-ellipsis whitespace-nowrap'>{props.data.sysname  }</p>
                </div>
            </section>
            <button className='mt-2 px-4 py-1 bg-blue-950 text-white-50 rounded-full transition-all duration-300 ease-in-out hover:bg-yellow-600'>Ver Detalles</button>
        </div>
    );
}