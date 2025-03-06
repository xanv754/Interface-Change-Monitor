export interface FilterFormProps {
    id: string;
    getValue: (value: string | null) => void;
}

export default function FilterForm(props: FilterFormProps) {
    const handlerFilter = (e: React.ChangeEvent<HTMLInputElement>) => {
        let value = e.target.value;
        if (value.length > 0) props.getValue(value);
        else props.getValue(null);
    }

    return (
        <div className="w-fit h-fit mt-1">
            <input 
                id={props.id}
                type="text"
                className="w-80 h-10 rounded-md bg-white-50 border-2 border-white-50 transition-all duration-200 px-4 outline-none overflow-hidden hover:border-yellow-500 focus:border-yellow-500"
                placeholder="Buscar por contenido"
                onChange={handlerFilter}
            />
        </div>
    );
}