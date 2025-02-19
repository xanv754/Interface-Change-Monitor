export interface SelectFormProps {
    id: string;
    label: string;
    options: string[];
  }
  
export default function SelectorForm(props: SelectFormProps) {
    return (
        <div className='w-fit flex flex-col lg:flex-row'>
        <label htmlFor={props.id} className='min-w-fit bg-blue-950 px-2 py-1 text-white-50 rounded-t-xl lg:rounded-l-xl lg:rounded-tr-none'>{props.label}</label>
        <select id={props.id} className='min-w-fit bg-white-100 px-4 py-1 appearance-none border-1 border-blue-950 rounded-b-xl lg:rounded-r-xl lg:lg:rounded-bl-none'>
            {props.options.map((option) => (
                <option key={option}>{option}</option>
            ))}
        </select>
        </div>
    );
}