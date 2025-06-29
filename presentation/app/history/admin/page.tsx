"use client";

import NavbarComponent from "@/app/components/navbar/navbar";
import InterfaceListComponent from "@/app/components/list/interfaces";
import AlertModalComponent from "@/app/components/modal/alert";
import { useState, useEffect, use } from "react";
import { SessionController } from "@/controllers/session";
import { HistoryController } from "@/controllers/history";
import { UserController } from "@/controllers/users";
import { SessionSchema } from "@/schemas/user";
import { InterfaceChangeSchema } from "@/schemas/interface";
import { UserSchema } from "@/schemas/user";

export default function HistoryPersonalPage() {
  const modalDefault = {
    showModal: false,
    title: "Cargando...",
    message: "Por favor, espere",
  };

  const [history, setHistory] = useState<InterfaceChangeSchema[]>([]);
  const [users, setUsers] = useState<UserSchema[]>([]);
  const [selectedUser, setSelectedUser] = useState<UserSchema | null>(null);
  const [modal, setModal] = useState(modalDefault);
  const [user, setUser] = useState<SessionSchema | null>(null);

  useEffect(() => {
    SessionController.getInfo().then((response) => {
      if (response) setUser(response);
      else SessionController.logout();
    });
    UserController.getAvailaibleAssignUsers().then((response) => {
      setUsers(response);
    });
  }, []);

  useEffect(() => {
    if (!selectedUser) return;
    HistoryController.getAllHistoryUsers([selectedUser.username]).then((response) => {
      setHistory(response);
    });
  }, [selectedUser]);

  return (
    <main className="w-full h-fit">
      <AlertModalComponent
        showModal={modal.showModal}
        title={modal.title}
        message={modal.message}
        onClick={() => {
          setModal(modalDefault);
        }}
      />
      <NavbarComponent user={user} />
      <div className="w-full p-2 flex flex-col gap-4">
        <section id="download" className="w-full bg-(--white) p-3.5 flex flex-row flex-nowrap justify-between items-center border-[0.2em] border-solid border-(--gray-light) rounded-lg shadow-[0.2em_0.3em_0.5em_rgba(0,0,0,0.2)]">
          <div id="description" className="flex flex-col">
            <h1 className="m-0 text-2xl text-(--blue)">Histórico del Día</h1>
            <p className="m-0 text-lg text-(--gray)">
              Descarga todos los datos de las interfaces con cambios detectados
              en el día.
            </p>
          </div>
          <button 
            className="w-fit h-full py-2 px-4 flex items-center rounded-lg bg-(--blue) text-(--white) text-lg transition-all duration-300 ease-in-out active:bg-(--blue-bright) hover:bg-(--blue-dark) disabled:bg-(--gray) disabled:text-(--gray-light)"
          >
            Descargar
          </button>
        </section>
        <section id="review" className="w-full bg-(--white) p-3.5 flex flex-col border-[0.2em] border-solid border-(--gray-light) rounded-lg shadow-[0.2em_0.3em_0.5em_rgba(0,0,0,0.2)] gap-3">
          <div id="description" className="flex flex-col">
            <h1 className="m-0 text-2xl text-(--blue)">Histórico de Asignaciones</h1>
            <p className="m-0 text-lg text-(--gray)">
              Seleccione un usuario para ver sus interfaces asignadas y su
              estatus de revisión en el mes.
            </p>
          </div>
          <div className="h-fit flex flex-row flex-nowrap justify-between items-center">
            <div className="w-fit h-[40px] flex flex-row flex-nowrap justify-start items-center has-[select:disabled]:label:bg-(--gray) has-[select:disabled]:label:text-(--gray-light)">
              <label 
                htmlFor="assign" 
                className="h-full m-0 px-4 flex items-center text-lg bg-(--blue) text-(--white) rounded-tl-xl rounded-bl-xl"
              >
                Usuario
              </label>
              <select 
                name="assing" 
                id="assing"
                className="min-w-2/6 h-full py-0 px-2 border-t-[0.2em] border-r-[0.2em] border-b-[0.2em] border-solid border-(--gray-light) bg-(--white) text-(--blue) text-lg rounded-tr-xl rounded-br-xl disabled:bg-(--gray-light) disabled:text-(--gray)"
                onClick={(e) => {
                  const selectedValue = (e.target as HTMLSelectElement).value;
                  if (!selectedValue || selectedValue === "")
                    setSelectedUser(null);
                  let user = users.find(
                    (user) => user.username === selectedValue
                  );
                  if (user) setSelectedUser(user);
                  else setSelectedUser(null);
                }}
              >
                <option value={""}>----</option>
                {users.map((user: UserSchema, index: number) => {
                  return (
                    <option key={index} value={user.username}>
                      {user.name} {user.lastname}
                    </option>
                  );
                })}
              </select>
            </div>
            <button 
              className="w-fit h-full py-2 px-4 flex items-center rounded-lg bg-(--blue) text-(--white) text-lg transition-all duration-300 ease-in-out active:bg-(--blue-bright) hover:bg-(--blue-dark) disabled:bg-(--gray) disabled:text-(--gray-light)"
              disabled={!selectedUser}
            >
              Descargar Historial de Usuario
            </button>
          </div>
        </section>
        <InterfaceListComponent
          title="Asignaciones Revisadas"
          interfaces={history}
          onChange={() => {}}
        />
      </div>
    </main>
  );
}
