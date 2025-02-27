import { UserResponseSchema } from '@/schemas/user';

export interface SelectOperatorProps {
    id: string;
    label: string;
    options: UserResponseSchema[];
    getValue: (value: string | null) => void;
  }
  
export default function SelectorOperatorForm(props: SelectOperatorProps) {
    const handlerValue = (event: React.ChangeEvent<HTMLSelectElement>) => {
        let value = event.target.value;
        if (value === 'empty') props.getValue(null);
        else props.getValue(value);
    };
    
    return (
        <div className='w-fit flex flex-col lg:flex-row'>
            <label htmlFor={props.id} className='min-w-fit bg-blue-950 px-4 py-1 text-white-50 rounded-t-xl lg:rounded-l-xl lg:rounded-tr-none'>{props.label}</label>
            <select 
                id={props.id} 
                onChange={handlerValue} 
                className='w-full bg-white-100 px-4 py-1 appearance-none border-1 border-blue-950 rounded-b-xl overflow-hidden text-ellipsis whitespace-nowrap lg:rounded-r-xl lg:lg:rounded-bl-none'>
                    <option value={'empty'}>----</option>
                    {props.options.map((user: UserResponseSchema) => (
                        <option key={user.username} value={user.username}>{user.name} {user.lastname}</option>
                    ))}
            </select>
        </div>
    );
}