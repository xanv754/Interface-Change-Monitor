import { UserSchema } from '@/schemas/user';

export interface SelectOperatorProps {
    id: string;
    label: string;
    options: UserSchema[];
  }
  
export default function SelectorOperatorForm(props: SelectOperatorProps) {
    return (
        <div className='w-full mb-2 flex flex-col lg:flex-row'>
        <label htmlFor={props.id} className='min-w-fit bg-blue-950 px-4 py-1 text-white-50 rounded-t-xl lg:rounded-l-xl lg:rounded-tr-none'>{props.label}</label>
        <select id={props.id} className='w-full bg-white-100 px-4 py-1 appearance-none border-1 border-blue-950 rounded-b-xl overflow-hidden text-ellipsis whitespace-nowrap lg:rounded-r-xl lg:lg:rounded-bl-none'>
            {props.options.map((user: UserSchema) => (
                <option key={user.username}>{user.name} {user.lastname}</option>
            ))}
        </select>
        </div>
    );
}