"use client";

import NavbarComponent from "@/app/components/navbar/navbar";
import HistoryInterfaceListComponent from "@/app/components/list/history";
import AlertModalComponent from "@/app/components/modal/alert";
import { useState, useEffect } from "react";
import { SessionController } from "@/controllers/session";
import { HistoryController } from "@/controllers/history";
import { AssignmentController } from "@/controllers/assignments";
import { SessionSchema } from "@/schemas/user";
import {
  InterfaceChangeSchema,
  InterfaceAssignedSchema,
} from "@/schemas/interface";
import { AssignmentStatusTypes } from "@/constants/types";
import { ExportHandler } from "@/utils/export";

export default function HistoryPersonalPage() {
  const modalDefault = {
    showModal: true,
    title: "Cargando...",
    message: "Por favor, espere",
  };

  const [history, setHistory] = useState<InterfaceAssignedSchema[]>([]);
  const [selectedInterfaces, setSelectedInterfaces] = useState<
    InterfaceChangeSchema[]
  >([]);
  const [selectedStatus, setSelectedStatus] = useState<string>("");
  const [modal, setModal] = useState(modalDefault);
  const [user, setUser] = useState<SessionSchema | null>(null);

  const handlerDownloadHistoryUser = async () => {
    if (history.length > 0 && user) {
      const url = await ExportHandler.exportHistoryUserToExcel(
        user.username,
        history,
      );
      if (url) {
        const a = document.createElement("a");
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
  };

  const handlerSubmitUpdateStatus = async (
    e: React.FormEvent<HTMLFormElement>,
  ) => {
    e.preventDefault();
    if (selectedInterfaces.length > 0 && selectedStatus !== "") {
      const statusResponse = await AssignmentController.updateStatusAssignments(
        selectedInterfaces,
        selectedStatus,
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
      setModal({ ...modalDefault, showModal: false });
    });
  }, []);

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
            <h1 className="font-display m-0 text-xl font-semibold text-(--ink)">
              Histórico de Asignaciones
            </h1>
            <p className="m-0 mt-1 text-sm text-(--gray)">
              Descarga todos los datos de las interfaces asignadas que ya ha
              revisado.
            </p>
          </div>
          <button
            onClick={() => {
              handlerDownloadHistoryUser();
            }}
            className="btn btn-primary"
          >
            Descargar
          </button>
        </section>
        <section className="card w-full p-5 flex flex-col gap-4">
          <div className="flex flex-col">
            <h1 className="font-display m-0 text-xl font-semibold text-(--ink)">
              Histórico de Asignaciones
            </h1>
            <p className="m-0 mt-1 text-sm text-(--gray)">
              Verique las interfaces asignadas revisadas en el mes. Seleccione
              las interfaces para cambiar su estatus de revisión.
            </p>
          </div>
          <form
            onSubmit={handlerSubmitUpdateStatus}
            className="flex flex-col sm:flex-row sm:items-end justify-end gap-3"
          >
            <div className="w-full sm:w-56 flex flex-col gap-1.5">
              <label htmlFor="assing" className="text-sm font-medium text-(--ink)">
                Cambiar Estatus
              </label>
              <select
                className="field select"
                name="assing"
                id="assing"
                disabled={selectedInterfaces.length <= 0}
                onChange={(e) => {
                  const selectedValue = (e.target as HTMLSelectElement)
                    .value as string;
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
                <option value={AssignmentStatusTypes.EQUIPMENT_DOWN}>
                  Equipo Caído
                </option>
              </select>
            </div>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={selectedInterfaces.length <= 0 || selectedStatus === ""}
            >
              Cambiar
            </button>
          </form>
        </section>
        <HistoryInterfaceListComponent
          title="Asignaciones Revisadas"
          interfaces={history}
          onChange={(interfaces: InterfaceChangeSchema[]) => {
            setSelectedInterfaces(interfaces);
          }}
        />
      </div>
    </main>
  );
}
