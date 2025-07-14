"use client";

import NavbarComponent from "@/app/components/navbar/navbar";
import HistoryInterfaceListComponent from "@/app/components/list/history";
import AlertModalComponent from "@/app/components/modal/alert";
import { useState, useEffect, use } from "react";
import { SessionController } from "@/controllers/session";
import { HistoryController } from "@/controllers/history";
import { AssignmentController } from "@/controllers/assignments";
import { SessionSchema } from "@/schemas/user";
import { InterfaceChangeSchema, InterfaceAssignedSchema } from "@/schemas/interface";
import { AssignmentStatusTypes } from "@/constants/types";
import { ExportHandler } from "@/utils/export";

export default function HistoryPersonalPage() {
  const modalDefault = {
    showModal: true,
    title: "Cargando...",
    message: "Por favor, espere",
  };

  const [history, setHistory] = useState<InterfaceAssignedSchema[]>([]);
  const [selectedInterfaces, setSelectedInterfaces] = useState<InterfaceChangeSchema[]>([]);
  const [selectedStatus, setSelectedStatus] = useState<string>("");
  const [modal, setModal] = useState(modalDefault);
  const [user, setUser] = useState<SessionSchema | null>(null);

  const handlerDownloadHistoryUser = async () => {
    if (history.length > 0 && user) {
      let url = await ExportHandler.exportHistoryUserToExcel(user.username, history);
      if (url) {
        const a = document.createElement('a');
        a.href = url;
        a.download = `Historial_de_${user.username}.xlsx`;
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

  const handlerSubmitUpdateStatus = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();
    if (selectedInterfaces.length > 0 && selectedStatus !== "") {
      let statusResponse = await AssignmentController.updateStatusAssignments(
        selectedInterfaces,
        selectedStatus
      );
      if (statusResponse) {
        setModal({
          showModal: true,
          title: "Interfaces Asignadas",
          message: "Las interfaces con cambios se han asignado correctamente.",
        });
      } else {
        setModal({
          showModal: true,
          title: "Error al Asignar Interfaces",
          message: "No se han podido asignar las interfaces.",
        });
      }
    }
  };

  useEffect(() => {
    SessionController.getInfo().then((response) => {
      if (response) setUser(response);
      else SessionController.logout();
    });
    HistoryController.getHistoryReviewedMonth().then((response) => {
      setHistory(response);
      setModal({...modalDefault, showModal: false});
    });
  }, []);

  return (
    <main className="w-full h-fit">
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
      <div className="w-full p-2 flex flex-col gap-4">
        <section
          id="download"
          className="w-full bg-(--white) p-3.5 flex flex-row flex-nowrap justify-between items-center border-[0.2em] border-solid border-(--gray-light) rounded-lg shadow-[0.2em_0.3em_0.5em_rgba(0,0,0,0.2)]"
        >
          <div id="description" className="flex flex-col">
            <h1 className="m-0 text-2xl text-(--blue)">
              Histórico de Asignaciones
            </h1>
            <p className="m-0 text-lg text-(--gray)">
              Descarga todos los datos de las interfaces asignadas que ya ha
              revisado.
            </p>
          </div>
          <button
            onClick={() => { handlerDownloadHistoryUser(); }}
            className="w-fit h-full py-2 px-4 flex items-center rounded-lg bg-(--blue) text-(--white) text-lg transition-all duration-300 ease-in-out active:bg-(--blue-bright) hover:bg-(--blue-dark) disabled:bg-(--gray) disabled:text-(--gray-light)"
          >
            Descargar
          </button>
        </section>
        <section
          id="review"
          className="w-full bg-(--white) p-3.5 flex flex-col border-[0.2em] border-solid border-(--gray-light) rounded-lg shadow-[0.2em_0.3em_0.5em_rgba(0,0,0,0.2)] gap-3"
        >
          <div id="description" className="flex flex-col">
            <h1 className="m-0 text-2xl text-(--blue)">
              Histórico de Asignaciones
            </h1>
            <p className="m-0 text-lg text-(--gray)">
              Verique las interfaces asignadas revisadas en el mes. Seleccione
              las interfaces para cambiar su estatus de revisión.
            </p>
          </div>
          <form onSubmit={handlerSubmitUpdateStatus} className="h-fit flex flex-row flex-nowrap justify-end items-center gap-2">
            <div className="w-fit h-[2.8rem] md:h-full flex flex-row flex-nowrap has-[select:disabled]:label:bg-(--gray) has-[select:disabled]:label:text-(--gray-light)">
              <label
                htmlFor="assign"
                className="h-full m-0 py-2 px-2 flex items-center bg-(--blue) text-(--white) rounded-tl-lg rounded-bl-lg"
              >
                Cambiar Estatus
              </label>
              <select
                className="min-w-2/6 h-[2.5rem] py-0 px-2 border-t-[0.2em] border-r-[0.2em] border-b-[0.2em] border-solid border-(--gray-light) bg-(--white) text-(--blue) text-lg rounded-tr-lg rounded-br-lg disabled:bg-(--gray-light) disabled:text-(--gray)"
                name="assing"
                id="assing"
                disabled={selectedInterfaces.length <= 0}
                onClick={(e) => {
                  const selectedValue = (e.target as HTMLSelectElement).value as string;
                  setSelectedStatus(selectedValue);
                }}
              >
                <option value={""}>----</option>
                <option value={AssignmentStatusTypes.INSPECTED}>
                  Inspeccionada
                </option>
                <option value={AssignmentStatusTypes.REDISCOVERED}>
                  Redescubierta
                </option>
              </select>
            </div>
            <button
              type="submit"
              className="w-fit h-full py-2 px-4 flex items-center rounded-lg bg-(--blue) text-(--white) text-lg transition-all duration-300 ease-in-out active:bg-(--blue-bright) hover:bg-(--blue-dark) disabled:bg-(--gray) disabled:text-(--gray-light)"
              disabled={selectedInterfaces.length <= 0 || selectedStatus === ""}
            >
              Cambiar
            </button>
          </form>
        </section>
        <HistoryInterfaceListComponent
          title="Asignaciones Revisadas"
          interfaces={history}
          onChange={(interfaces: InterfaceChangeSchema[]) => {setSelectedInterfaces(interfaces)}}
        />
      </div>
    </main>
  );
}
