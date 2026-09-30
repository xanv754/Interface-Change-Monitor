import React, { useEffect } from 'react';

/**
 * @interface Data required for the alert modal.
 *
 * @param {boolean} showModal if the modal is visible.
 * @param {string} title Title of the modal.
 * @param {string} message Message of the modal.
 */
interface ModalProps {
    showModal: boolean;
    title: string;
    message: string;
    onClick?: () => void;
}

export default function AlertModalComponent(props: ModalProps) {

    const handlerAccept = () => {
        document.getElementById('modal-state')?.classList.add('hidden');
        if (props.onClick) props.onClick();
    }

    useEffect(() => {
        const modalAccept = document.getElementById('modal-accept');
        const modalState = document.getElementById('modal-state');

        if (modalAccept && modalState) {
            modalAccept.addEventListener('click', handlerAccept);

            if (props.showModal) modalState.classList.remove('hidden');
            else modalState.classList.add('hidden');
        }

        return () => {
            modalAccept?.removeEventListener('click', handlerAccept);
        };

    }, [props.showModal]);

    return(
        <div id="modal-state" className="absolute z-40" aria-labelledby="modal-title" role="dialog" aria-modal="true">
            <aside className="fixed inset-0 bg-(--ink)/50 backdrop-blur-[2px] transition-opacity" aria-hidden="true"></aside>
            <div className="fixed inset-0 z-40 w-screen overflow-y-auto">
                <div id="modal-panel" className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
                    <div className="relative transform overflow-hidden rounded-xl bg-(--white) text-left shadow-[var(--shadow-modal)] transition-all sm:my-8 sm:w-full sm:max-w-md">
                        <section className="px-6 pt-6 pb-4">
                            <h3 className="font-display m-0 text-lg font-semibold text-(--ink)" id="modal-title">{props.title}</h3>
                            <p className="mt-2 mb-0 text-sm text-(--gray)">{props.message}</p>
                        </section>
                        <section className="px-6 pb-6 flex justify-end">
                            <button
                                id="modal-accept"
                                type="button"
                                className="btn btn-primary"
                            >
                                Aceptar
                            </button>
                        </section>
                    </div>
                </div>
            </div>
        </div>
    );
}
