"use client";

import NavbarComponent from "@/app/components/navbar/navbar";
import CardComponent from "@/app/components/card/main";
import InterfaceListComponent from "@/app/components/list/interfaces";
import AlertModalComponent from "@/app/components/modal/alert";
import { useState, useEffect } from "react";
import { StatusOption } from "@/app/components/card/main";
import { HistoryController } from "@/controllers/history";
import { AssignmentController } from "@/controllers/assignments";
import { StatisticsController } from "@/controllers/statistics";
import { SessionController } from "@/controllers/session";
import { InterfaceChangeSchema } from "@/schemas/interface";
import { StatisticsAssignmentSchema } from "@/schemas/assignment";
import { SessionSchema } from "@/schemas/user";
import { OperationData } from "@/utils/operation";
import { AssignmentStatusTypes } from "@/constants/types";

export default function DashboardPage() {
  const modalDefault = {
    showModal: true,
    title: "Cargando...",
    message: "Por favor, espere",
  };

  const [assignments, setAssignments] = useState<InterfaceChangeSchema[]>([]);
  const [viewAssignments, setViewAssignments] = useState<
    InterfaceChangeSchema[]
  >([]);
  const [statistics, setStatistics] =
    useState<StatisticsAssignmentSchema | null>(null);
  const [selectedInterfaces, setSelectedInterfaces] = useState<
    InterfaceChangeSchema[]
  >([]);
  const [selectedStatus, setSelectedStatus] = useState<string>("");
  const [modal, setModal] = useState(modalDefault);
  const [user, setUser] = useState<SessionSchema | null>(null);

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

  const handlerGetTotalReviewedStatistics = () => {
    if (!statistics) return 0;
    const total_inspected = statistics.total_inspected_month ?? 0;
    const total_rediscovered = statistics.total_rediscovered_month ?? 0;
    return total_inspected + total_rediscovered;
  };

  useEffect(() => {
    SessionController.getInfo().then((response) => {
      if (response) setUser(response);
      else SessionController.logout();
    });
    StatisticsController.getStatisticPersonal().then((response) => {
      setStatistics(response);
    });
    HistoryController.getHistoryPending().then((response) => {
      setAssignments(response);
      setViewAssignments(response);
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
      <div className="max-w-7xl mx-auto px-4 md:px-6 py-6 flex flex-col gap-6">
        <section className="w-full flex flex-row flex-wrap gap-4">
          <CardComponent
            title="Interfaces Asignadas Hoy"
            total={statistics?.total_pending_today ?? 0}
            status={StatusOption.NORMAL}
          />
          <CardComponent
            title="Interfaces Pendientes en el Mes"
            total={statistics?.total_pending_month ?? 0}
            status={StatusOption.PENDING}
          />
          <CardComponent
            title="Interfaces Revisadas en el Mes"
            total={handlerGetTotalReviewedStatistics()}
            status={StatusOption.REVIEW}
          />
        </section>
        <section className="card w-full p-5 flex flex-col gap-4">
          <div>
            <h3 className="font-display m-0 text-xl font-semibold text-(--ink)">
              Asignación de Interfaces
            </h3>
            <p className="m-0 mt-1 text-sm text-(--gray)">
              Seleccione interfaces con cambios para asignar a un usuario o asigne
              automáticamente todas las interfaces con cambios a los usuarios
              disponibles.
            </p>
          </div>
          <div className="flex flex-col md:flex-row md:items-end gap-3 md:justify-between">
            <div className="w-full md:w-64 flex flex-col gap-1.5">
              <label htmlFor="search" className="text-sm font-medium text-(--ink)">
                Buscar
              </label>
              <input
                id="search"
                type="text"
                className="field"
                placeholder="Dato de la interfaz"
                onChange={(e) => {
                  const filter = e.target.value;
                  if (!filter) setViewAssignments(assignments);
                  else
                    setViewAssignments(
                      OperationData.filterChangeInterfaces(assignments, filter),
                    );
                }}
              />
            </div>
            <form
              className="flex flex-col sm:flex-row sm:items-end gap-3"
              onSubmit={(e) => handlerSubmitUpdateStatus(e)}
            >
              <div className="w-full sm:w-56 flex flex-col gap-1.5">
                <label htmlFor="assing" className="text-sm font-medium text-(--ink)">
                  Cambiar Estatus
                </label>
                <select
                  className="field select"
                  name="assing"
                  id="assing"
                  disabled={assignments.length <= 0}
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
          </div>
        </section>
        <section>
          <InterfaceListComponent
            title="Interfaces con Cambios"
            interfaces={viewAssignments}
            onChange={(interfaces: InterfaceChangeSchema[]) =>
              setSelectedInterfaces(interfaces)
            }
          />
        </section>
      </div>
    </main>
  );
}
