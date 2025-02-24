import { use, useEffect, useState } from "react";

export type InputType = 'text' | 'password';

export interface InputFormProps {
  id: string;
  label: string;
  type: InputType;
  defaultValue: string;
  getInput: (content: string | null) => void
  validateInput: (content: string) => boolean;
  disabled: boolean;
  placeholder?: string;
}

export default function InputTextStateForm(props: InputFormProps) {
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
        if (props.disabled && props.defaultValue) {
            document.getElementById(`input-${props.id}`)?.setAttribute("value", props.defaultValue);
        }
    }, [props.disabled]);

    useEffect(() => {
        if (props.placeholder) {
            document.getElementById(`input-${props.id}`)?.setAttribute("placeholder", props.placeholder);
        }
    }, []);

    return (
        <div className="min-w-fit w-80">
            {!props.disabled &&
                <label htmlFor={props.id} className={`block ${(error && !props.disabled) ? "text-red-500" : "text-blue-800"} font-semibold text-sm`}>
                    {props.label}: {props.defaultValue}
                </label>
            }
            {props.disabled &&
                <label htmlFor={props.id} className={`block ${(error && !props.disabled) ? "text-red-500" : "text-blue-800"} font-semibold text-sm`}>
                    {props.label}
                </label>
            }
            <div className='mt-1'>
                <input
                    id={`input-${props.id}`}
                    type={props.type}
                    name={props.id}
                    className={`block w-full rounded-md py-1.5 px-2 ring-1 ring-inset ${(error && !props.disabled) ? "ring-red-500" : "ring-gray-400"} focus:ring-blue-950 placeholder:text-sm`}
                    onChange={validate}
                    disabled={props.disabled}
                />
            </div>
        </div>
    );
}