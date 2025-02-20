import { useEffect, useState } from "react";

export type InputType = 'text' | 'password';

export interface InputFormProps {
  id: string;
  label: string;
  type: InputType;
  getInput: (content: string | null) => void
  validateInput: (content: string) => boolean;
  messageError: string;
  placeholder?: string;
}

export default function InputTextForm(props: InputFormProps) {
    const [error, setError] = useState<boolean>(false);

    const content = (content: string | null) => {
        props.getInput && props.getInput(content);
    };

    const validate = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (props.validateInput(event.target.value)) {
            setError(false);
            content(event.target.value);
        } else {
            setError(true);
            content(null);
        }
    };

    useEffect(() => {
        if (props.placeholder) {
            document.getElementById(`input-${props.id}`)?.setAttribute("placeholder", props.placeholder);
        }
    }, []);

    return (
        <div className="min-w-fit w-80">
            <label htmlFor={props.id} className={`block ${error ? "text-red-500" : "text-blue-800"} font-semibold text-sm`}>{props.label}</label>
            <div className='mt-1'>
                <input
                    id={`input-${props.id}`}
                    type={props.type}
                    name={props.id}
                    className={`block w-full rounded-md py-1.5 px-2 ring-1 ring-inset ${error ? "ring-red-500" : "ring-gray-400"} focus:ring-blue-950 placeholder:text-sm`}
                    onChange={validate}
                />
            </div>
            <small id={`error-${props.id}`} className={`pt-1 ${!error ? "invisible" : "visible"} text-red-500 text-sm`}>{props.messageError}</small>
        </div>
    );
}