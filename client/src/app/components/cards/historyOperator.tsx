export interface HistoryOperatorCardProps {
    getValue: (value: string) => void;
    username?: string;
    name?: string;
    lastname?: string;
}

export default function HistoryOperatorCard(props: HistoryOperatorCardProps) {
    const downloadHistory = (username?: string) => {
        if (username) props.getValue(username);
    }

    return (
        <>{props.username && props.name && props.lastname &&
            <div className="w-96 h-fit bg-white-50 rounded-lg flex flex-col items-center justify-center gap-2 p-4 shadow-md drop-shadow-[1px_1px_2px_rgba(0,0,0,0.25)]">
                <h3 className='text-gray-700 font-bold'>{props.name} {props.lastname}</h3>
                <button 
                    onClick={() => downloadHistory(props.username)}
                    className="bg-blue-800 text-white-50 font-bold px-10 py-1 rounded-full transition-all duration-300 ease-in-out hover:bg-blue-950">
                        Descargar
                </button>
            </div>
        }</>
    );
}