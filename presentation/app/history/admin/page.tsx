"use client";

import NavbarComponent from "@/app/components/navbar/navbar";
import HistoryInterfaceListComponent from "@/app/components/list/history";
import AlertModalComponent from "@/app/components/modal/alert";
import { useState, useEffect } from "react";
import { SessionController } from "@/controllers/session";
import { HistoryController } from "@/controllers/history";
import { UserController } from "@/controllers/users";
import { SessionSchema } from "@/schemas/user";
import { InterfaceController } from "@/controllers/interfaces";
import { InterfaceChangeSchema, InterfaceAssignedSchema } from "@/schemas/interface";
import { UserSchema } from "@/schemas/user";
import { DateHandler } from "@/utils/date";
import { ExportHandler } from "@/utils/export";

export default function HistoryPersonalPage() {
  const modalDefault = {
    showModal: true,
    title: "Cargando...",
    message: "Por favor, espere",
  };

  const [changes, setChanges] = useState<InterfaceChangeSchema[]>([]);
  const [history, setHistory] = useState<InterfaceAssignedSchema[]>([]);
  const [users, setUsers] = useState<UserSchema[]>([]);
  const [selectedUser, setSelectedUser] = useState<UserSchema | null>(null);
  const [modal, setModal] = useState(modalDefault);
  const [user, setUser] = useState<SessionSchema | null>(null);

  const handlerDownloadHistoryUser = async () => {
    const historyUser = history.filter((assignment) => assignment.username === selectedUser?.username);
    if (historyUser.length > 0 && selectedUser) {
      let url = await ExportHandler.exportHistoryUserToExcel(selectedUser.username, historyUser);
      if (url) {
        const a = document.createElement('a');
        a.href = url;
        a.download = `Historial_de_${selectedUser.username}.xlsx`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      } else {
        setModal({
          showModal: true,
          title: "Error al Descargar Historial de Usuario",
          message: "No se pudo descargar el archivo.",
        });
      }
    }
  }

  const handlerDowndloadInterfaceChanges = async () => {
    if (changes.length > 0) {
      let url = await ExportHandler.exportInterfaceChangesToExcel(changes);
      if (url) {
        const date = DateHandler.getNow();
        const a = document.createElement('a');
        a.href = url;
        a.download = `Cambios_de_Interfaces_${date}.xlsx`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      } else {
        setModal({
          showModal: true,
          title: "Error al Descargar Cambios del Día",
          message: "No se pudo descargar el archivo.",
        });
      }
    }
  };

  useEffect(() => {
    SessionController.getInfo().then((response) => {
      if (response) setUser(response);
      else SessionController.logout();
    });
    UserController.getAvailaibleAssignUsers().then((response) => {
      setUsers(response);
    });
    InterfaceController.getInterfaceChanges().then((response) => {
      setChanges(response);
      setModal({...modalDefault, showModal: false});
    });
  }, []);

  useEffect(() => {
    if (!selectedUser) { 
      setHistory([]);
      return;
    }
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
            onClick={() => { handlerDowndloadInterfaceChanges(); }}
            className="w-fit h-full py-2 px-4 flex items-center rounded-lg bg-(--blue) text-(--white) text-lg transition-all duration-300 ease-in-out cursor-pointer active:bg-(--blue-bright) hover:bg-(--blue-dark) disabled:bg-(--gray) disabled:text-(--gray-light) disabled:cursor-not-allowed"
            disabled={changes.length <= 0}
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
              onClick={() => { handlerDownloadHistoryUser(); }}
              className="w-fit h-full py-2 px-4 flex items-center rounded-lg bg-(--blue) text-(--white) text-lg transition-all duration-300 ease-in-out cursor-pointer active:bg-(--blue-bright) hover:bg-(--blue-dark) disabled:bg-(--gray) disabled:text-(--gray-light) disabled:cursor-not-allowed"
              disabled={!selectedUser || history.length <= 0}
            >
              Descargar Historial de Usuario
            </button>
          </div>
        </section>
        <HistoryInterfaceListComponent
          title="Asignaciones Revisadas"
          interfaces={history}
          onChange={() => {}}
        />
      </div>
    </main>
  );
}
