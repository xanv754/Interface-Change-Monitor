import React, { useEffect } from 'react';

interface AlertModelProps {
    showModal: boolean;
    afterAction?: () => void;
}

export default function LoadingModal(props: AlertModelProps) {
    useEffect(() => {
        const modalState = document.getElementById('modal-state');

        if (modalState) {
            if (props.showModal) modalState.classList.remove('hidden');
            else modalState.classList.add('hidden');
        }

    }, [props.showModal]);

    return(
        <div id="modal-state" className="absolute z-10" aria-labelledby="modal-title" role="dialog" aria-modal="true">
            <aside className="fixed inset-0 bg-black-950 bg-opacity-55 transition-opacity" aria-hidden="true"></aside>
            <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
                <div id="modal-panel" className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
                    <div className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
                        <section className="bg-gray-50 px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                            <div className="sm:flex sm:items-start">
                                <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                                    <h3 className="text-lg text-blue-800 font-semibold leading-6" id="modal-title">Cargando</h3>
                                    <div className="mt-2">
                                        <p className="text-sm text-gray-500">Obteniendo información. Por favor, espere...</p>
                                    </div>
                                </div>
                            </div>
                        </section>
                    </div>
                </div>
            </div>
        </div>
    );
}