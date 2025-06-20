"use client";

import NavbarAdminComponent from "../../components/navbar/admin";
import CardComponent from "../../components/card/main";
import InterfacesListComponent from "../../components/list/interfaces";
import AlertModalComponent from "@/app/components/modal/alert";
import styles from './dashboard.module.css';
import { useState, useEffect } from "react";
import { StatusOption } from "../../components/card/main";
import { ChangeController } from "@/controllers/changes";
import { UserController } from "@/controllers/users";
import { AssignmentController } from "@/controllers/assignments";
import { ChangeInterface } from "@/models/changes";
import { UserModel } from "@/models/users";
import { NewAssignmentModel } from "@/models/assignments";
import { AssignmentStatusTypes } from "@/constants/types";
import { OperationData } from "@/utils/operation";
import { DateHandler } from "@/utils/date";


export default function DashboardPage() {
    const modalDefault = { showModal: false, title: "", message: "" };

    const [changeInterfaces, setChangeInterfaces] = useState<ChangeInterface[]>([]);
    const [viewInterfaces, setViewInterfaces] = useState<ChangeInterface[]>([]);
    const [selectedInterfaces, setSelectedInterfaces] = useState<ChangeInterface[]>([]);
    const [availableUsers, setAvailableUsers] = useState<UserModel[]>([]);
    const [selectedUser, setSelectedUser] = useState<UserModel | null>(null);
    const [modal, setModal] = useState(modalDefault);

    const handlerSubmitAssignments = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const assignments: NewAssignmentModel[] = [];
        if (selectedInterfaces.length > 0 && selectedUser) {
            selectedInterfaces.map(interfaceChange => {
                assignments.push({
                    old_interface_id: Number(interfaceChange.id_old),
                    current_interface_id: Number(interfaceChange.id_new),
                    username: selectedUser.username,
                    assign_by: "test frontend",
                    type_status: AssignmentStatusTypes.PENDING
                });
            });
            let statusResponse = await AssignmentController.newAssignments(assignments);
            if (statusResponse) {
                setModal({ showModal: true, title: "Interfaces Asignadas", message: "Las interfaces con cambios se han asignado correctamente." });
            } else {
                setModal({ showModal: true, title: "Error al Asignar Interfaces", message: "No se han podido asignar las interfaces." });
            }
        }
    }

    useEffect(() => {
        ChangeController.getChanges().then(response => { 
            setChangeInterfaces(response);
            setViewInterfaces(response);
        });
        UserController.getUsers().then(response => { setAvailableUsers(response) });
    }, []);


    return (
        <main>
            <AlertModalComponent showModal={modal.showModal} title={modal.title} message={modal.message} onClick={() => { setModal(modalDefault) }} />
            <NavbarAdminComponent />
            <section className={styles.cardStatistics}>
                <CardComponent title="Interfaces con Cambios Detectados Hoy" total={changeInterfaces.length} status={StatusOption.NORMAL} />
                <CardComponent title="Interfaces Pendientes en el Mes" total={5} status={StatusOption.PENDING} />
                <CardComponent title="Interfaces Revisadas en el Mes" total={5} status={StatusOption.REVIEW} />
            </section>
            <section className={styles.assignment}>
                <h3>Asignación de Interfaces</h3>
                <p>Seleccione interfaces con cambios para asignar a un usuario o asigne automáticamente todas las interfaces con cambios a los usuarios disponibles.</p>
                <div className="h-14 p-0 pt-4 flex flex-row flex-wrap justify-between">
                    <div className={styles.box}>
                        <label htmlFor="assign">Buscar</label>
                        <input 
                            type="text" 
                            className={styles.inputFilter} 
                            placeholder="Dato de la interfaz"
                            onChange={(e) => {
                                const filter = e.target.value;
                                if (!filter) setViewInterfaces(changeInterfaces);
                                else setViewInterfaces(OperationData.filterChangeInterfaces(changeInterfaces, filter));
                            }}
                        />
                    </div>
                    <button className={styles.btn} disabled={(!changeInterfaces || changeInterfaces.length <= 0) && (!availableUsers || availableUsers.length <= 0)}>Asignación Automática</button>
                    <form className={styles.confirmAssignment} onSubmit={(e) => handlerSubmitAssignments(e)}>
                        <div className={styles.box}>
                            <label htmlFor="assign">Asignar a</label>
                            <select 
                                name="assing" 
                                id="assing" 
                                disabled={(!changeInterfaces || changeInterfaces.length <= 0) && (!availableUsers || availableUsers.length <= 0)}
                                onClick={(e) => {
                                    const selectedValue = (e.target as HTMLSelectElement).value;
                                    if (!selectedValue || selectedValue === "") setSelectedUser(null);
                                    let user = availableUsers.find(user => user.username === selectedValue);
                                    if (user) setSelectedUser(user);
                                    else setSelectedUser(null);
                                }}
                            >
                                <option value={""}>----</option>
                                {availableUsers.map((user: UserModel, index: number) => {
                                    return (
                                        <option key={index} value={user.username}>{user.name} {user.lastname}</option>
                                    );
                                })}
                            </select>
                        </div>
                        <button type="submit" className={styles.btn} disabled={(!selectedInterfaces || selectedInterfaces.length <= 0) || !selectedUser }>Asignar</button>
                    </form>
                </div>
            </section>
            <section className={styles.listInterfaces}>
                <InterfacesListComponent title="Interfaces con Cambios" interfaces={viewInterfaces} onChange={(interfaces: ChangeInterface[]) => setSelectedInterfaces(interfaces)} />
            </section>
        </main>
    );
}