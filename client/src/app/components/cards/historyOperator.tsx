import { UserResponseSchema } from "@/schemas/user";

export interface HistoryOperatorCardProps {
    user: UserResponseSchema;
    getValue: (value: string) => void;
}

export default function HistoryOperatorCard(props: HistoryOperatorCardProps) {
    return (
        <div className="w-96 h-fit bg-white-100 rounded-lg flex flex-col items-center justify-center gap-2 p-4 shadow-md drop-shadow-[1px_1px_2px_rgba(0,0,0,0.25)]">
            <h3 className='text-gray-700 font-bold'>{props.user.name} {props.user.lastname}</h3>
            <button className="bg-blue-800 text-white-50 font-bold px-10 py-1 rounded-full transition-all duration-300 ease-in-out hover:bg-blue-950">
                Descargar
            </button>
        </div>
    );
}