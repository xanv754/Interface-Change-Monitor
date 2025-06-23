"use client";

import NavbarComponent from "@/app/components/navbar/navbar";
import CardComponent from "@/app/components/card/main";
import InterfaceAssignmentListComponent from "@/app/components/list/assignments";
import AlertModalComponent from "@/app/components/modal/alert";
import { useState, useEffect } from "react";
import { StatusOption } from "@/app/components/card/main";
import { SessionController } from "@/controllers/session";
import { AssignmentController } from "@/controllers/assignments";
import { AssignmentModel } from "@/models/assignments";
import { UserLoggedModel } from "@/models/users";


export default function DashboardPage() {
    const modalDefault = { showModal: false, title: "Cargando...", message: "Por favor, espere" };

    const [assignments, setAssignments] = useState<AssignmentModel[]>([]);
    const [selectedInterfaces, setSelectedInterfaces] = useState<AssignmentModel[]>([]);
    const [modal, setModal] = useState(modalDefault);
    const [user, setUser] = useState<UserLoggedModel | null>(null);

    useEffect(() => {
        SessionController.getUser().then(response => {
            if (response) setUser(response);
            else SessionController.logout();
        });
        AssignmentController.getPending().then(response => {
            setAssignments(response);
        });
    }, []);


    return (
        <main>
            <AlertModalComponent showModal={modal.showModal} title={modal.title} message={modal.message} onClick={() => { setModal(modalDefault) }} />
            <NavbarComponent user={user} />
            <section className="w-full py-2 px-4 flex flex-row flex-wrap gap-2 lg:gap-4">
                <CardComponent title="Interfaces Asignadas Hoy" total={12} status={StatusOption.NORMAL} />
                <CardComponent title="Interfaces Pendientes" total={5} status={StatusOption.PENDING} />
                <CardComponent title="Interfaces Revisadas" total={5} status={StatusOption.REVIEW} />
            </section>
            <section className="w-full min-h-fit p-[1em] flex flex-col justify-between">
                <h3 className="m-0 text-3xl font-bold text-(--blue)">Interfaces Asignadas</h3>
                <p className="m-0 text-lg text-(--gray)">Seleccione interfaces para cambiar su estatus.</p>
                <div className="h-fit md:h-14 p-0 pt-4 flex flex-col gap-2 md:flex-row md:gap-0 md:justify-between">
                    <div className="w-fit h-[2.8rem] md:h-full flex flex-row flex-nowrap has-[select:disabled]:label:bg-(--gray) has-[select:disabled]:label:text-(--gray-light)">
                        <label htmlFor="assign" className="h-full m-0 py-2 px-2 flex items-center bg-(--blue) text-(--white) rounded-tl-lg rounded-bl-lg">Buscar</label>
                        <input 
                            type="text" 
                            className="bg-(--white) py-0 px-2 text-(--gray) border-t-[0.2em] border-r-[0.2em] border-b-[0.2em] border-solid border-(--gray-light) rounded-tr-lg rounded-br-lg"
                            placeholder="Dato de la interfaz"
                        />
                    </div>
                    <div className="w-fit h-full flex flex-col md:flex-row gap-2">
                        <div className="w-fit min-w-fit h-full flex flex-row flex-nowrap">
                            <label htmlFor="assign" className="h-[2.7rem] md:h-full m-0 py-2 px-2 flex items-center bg-(--blue) text-(--white) rounded-tl-lg rounded-bl-lg">Estatus</label>
                            <select 
                                className="min-w-2/6 h-[2.7rem] md:h-full py-0 px-2 border-t-[0.2em] border-r-[0.2em] border-b-[0.2em] border-solid border-(--gray-light) bg-(--white) text-(--blue) text-lg rounded-tr-lg rounded-br-lg disabled:bg-(--gray-light) disabled:text-(--gray)"
                                name="assing" 
                                id="assing"
                            >
                                <option value="user1">Revisada</option>
                                <option value="user2">Redescubierta</option>
                            </select>
                        </div>
                        <button 
                            className="w-fit h-full py-2 px-4 flex items-center rounded-lg bg-(--blue) text-(--white) text-lg transition-all duration-300 ease-in-out active:bg-(--blue-bright) hover:bg-(--blue-dark) disabled:bg-(--gray) disabled:text-(--gray-light)" 
                            disabled
                        >Cambiar Estatus</button>
                    </div>
                </div>
            </section>
            <section className="min-h-fit py-0 px-4">
                <InterfaceAssignmentListComponent title="Interfaces Pendientes" interfaces={assignments} onChange={(interfaces: AssignmentModel[]) => setSelectedInterfaces(interfaces)} />
            </section>
        </main>
    );
}