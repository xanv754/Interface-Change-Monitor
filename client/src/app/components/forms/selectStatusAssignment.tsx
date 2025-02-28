import { StatusAssignment, StatusAssignmentTranslation } from '@libs/types';

export interface SelectFormProps {
    id: string;
    label: string;
    getValue: (value: string | null) => void;
  }
  
export default function SelectorStatusAssignmentForm(props: SelectFormProps) {
    const handlerValue = (event: React.ChangeEvent<HTMLSelectElement>) => {
        let value = event.target.value;
        if (value === 'empty') props.getValue(null);
        else props.getValue(value);
    };
    
    return (
        <div className='w-fit flex flex-col lg:flex-row'>
            <label htmlFor={props.id} className='min-w-fit bg-blue-800 px-2 py-1 text-white-50 rounded-t-xl lg:rounded-l-xl lg:rounded-tr-none'>{props.label}</label>
            <select 
                id={props.id} 
                onChange={handlerValue}
                className='min-w-fit bg-white-100 px-4 py-1 appearance-none border-1 border-blue-950 rounded-b-xl lg:rounded-r-xl lg:lg:rounded-bl-none'>
                    <option value={'empty'}>----</option>
                    <option value={StatusAssignment.pending}>{StatusAssignmentTranslation.pending}</option>
                    <option value={StatusAssignment.inspected}>{StatusAssignmentTranslation.inspected}</option>
                    <option value={StatusAssignment.rediscovered}>{StatusAssignmentTranslation.rediscovered}</option>
            </select>
        </div>
    );
}