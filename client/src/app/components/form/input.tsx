import { useState } from "react";

export type InputType = 'text' | 'password';

export interface InputFormProps {
  id: string;
  label: string;
  type: InputType;
  getInput: (content: string) => void
  validateInput: (content: string) => boolean;
  messageError: string;
}

export default function InputTextForm(props: InputFormProps) {
    const [error, setError] = useState<boolean>(false);

    const content = (event: React.ChangeEvent<HTMLInputElement>) => {
        props.getInput && props.getInput(event.target.value);
    };

    const validate = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (props.validateInput(event.target.value)) {
            setError(false);
            content(event);
        } else {
            setError(true);
        }
    };

    return (
        <div className="min-w-fit w-80">
            <label htmlFor={props.id} className={`block ${error ? "text-red-500" : "text-blue-800"} font-semibold text-sm`}>{props.label}</label>
            <div className='mt-1'>
                <input
                    type={props.type}
                    name={props.id}
                    className={`block w-full rounded-md py-1.5 px-2 ring-1 ring-inset ${error ? "ring-red-500" : "ring-gray-400"} focus:ring-blue-950 `}
                    onChange={validate}
                />
            </div>
            <small id={`error-${props.id}`} className={`pt-1 ${!error ? "invisible" : "visible"} text-red-500 text-sm`}>{props.messageError}</small>
        </div>
    );
}