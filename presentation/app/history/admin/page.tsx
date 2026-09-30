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

export default function HistoryAdminPage() {
  const modalDefault = {
    showModal: true,
    title: "Cargando...",
    message: "Por favor, espere",
  };

  const [changes, setChanges] = useState<InterfaceChangeSchema[]>([]);
  const [history, setHistory] = useState<InterfaceAssignedSchema[]>([]);
  const [users, setUsers] = useState<UserSchema[]>([]);
  const [datesAvailable, SetDatesAvailable] = useState<string[]>([]);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [selectedUser, setSelectedUser] = useState<UserSchema | null>(null);
  const [modal, setModal] = useState(modalDefault);
  const [user, setUser] = useState<SessionSchema | null>(null);

  const handlerDownloadHistoryUser = async () => {
    if (history.length > 0 && selectedUser) {
      const url = await ExportHandler.exportHistoryUserToExcel(selectedUser.username, history);
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
      const url = await ExportHandler.exportInterfaceChangesToExcel(changes);
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
    InterfaceController.getAllInterfaceChanges().then((response) => {
      setChanges(response);
      setModal({ ...modalDefault, showModal: false });
    });
    HistoryController.getDateAvailableToConsultHistory().then((response) => {
      SetDatesAvailable(response);
    });
  }, []);

  useEffect(() => {
    if (!selectedUser || !selectedDate) {
      setHistory([]);
      return;
    }
    HistoryController.getAllHistoryUsers([selectedUser.username], selectedDate).then((response) => {
      setHistory(response);
    });
  }, [selectedUser, selectedDate]);

  return (
    <main className="w-full min-h-screen">
      <AlertModalComponent
        showModal={modal.showModal}
        title={modal.title}
        message={modal.message}
        onClick={() => {
          setModal(modalDefault);
          window.location.reload();
        }}
      />
      <NavbarComponent user={user} />
      <div className="max-w-7xl mx-auto px-4 md:px-6 py-6 flex flex-col gap-4">
        <section className="card w-full p-5 flex flex-row flex-wrap justify-between items-center gap-4">
          <div className="flex flex-col">
            <h1 className="font-display m-0 text-xl font-semibold text-(--ink)">Histórico del Día</h1>
            <p className="m-0 mt-1 text-sm text-(--gray)">
              Descarga todos los datos de las interfaces con cambios detectados
              en el día.
            </p>
          </div>
          <button
            onClick={() => { handlerDowndloadInterfaceChanges(); }}
            className="btn btn-primary"
            disabled={changes.length <= 0}
          >
            Descargar
          </button>
        </section>
        <section className="card w-full p-5 flex flex-col gap-4">
          <div className="flex flex-col">
            <h1 className="font-display m-0 text-xl font-semibold text-(--ink)">Histórico de Asignaciones</h1>
            <p className="m-0 mt-1 text-sm text-(--gray)">
              Seleccione un usuario para ver sus interfaces asignadas y su
              estatus de revisión en el mes.
            </p>
          </div>
          <div className="flex flex-col md:flex-row md:items-end gap-3">
            <div className="w-full md:w-56 flex flex-col gap-1.5">
              <label htmlFor="assing" className="text-sm font-medium text-(--ink)">
                Usuario
              </label>
              <select
                id="assing"
                name="assing"
                className="field select"
                onChange={(e) => {
                  const selectedValue = (e.target as HTMLSelectElement).value;
                  if (!selectedValue || selectedValue === "")
                    setSelectedUser(null);
                  const user = users.find(
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
            <div className="w-full md:w-40 flex flex-col gap-1.5">
              <label htmlFor="date" className="text-sm font-medium text-(--ink)">
                Mes
              </label>
              <select
                id="date"
                name="date"
                className="field select"
                onChange={(e) => {
                  const selectedValue = (e.target as HTMLSelectElement).value;
                  if (!selectedValue) setSelectedDate(null);
                  else setSelectedDate(selectedValue);
                }}
              >
                <option value={""}>----</option>
                {datesAvailable.map((date: string, index: number) => {
                  return (
                    <option key={index} value={date}>
                      {date}
                    </option>
                  );
                })}
              </select>
            </div>
            <button
              onClick={() => { handlerDownloadHistoryUser(); }}
              className="btn btn-primary"
              disabled={!selectedUser || history.length <= 0}
            >
              Descargar Historial de Usuario
            </button>
          </div>
        </section>
        <HistoryInterfaceListComponent
          title="Asignaciones Revisadas"
          interfaces={history}
          onChange={() => { }}
        />
      </div>
    </main>
  );
}
