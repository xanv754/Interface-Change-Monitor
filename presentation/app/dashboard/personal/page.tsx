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
  const [viewAssignments, setViewAssignments] = useState<InterfaceChangeSchema[]>([]);
  const [statistics, setStatistics] = useState<StatisticsAssignmentSchema | null>(null);
  const [selectedInterfaces, setSelectedInterfaces] = useState<InterfaceChangeSchema[]>([]);
  const [selectedStatus, setSelectedStatus] = useState<string>("");
  const [modal, setModal] = useState(modalDefault);
  const [user, setUser] = useState<SessionSchema | null>(null);

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
      <section className="w-full py-2 px-4 flex flex-row flex-wrap gap-2 lg:gap-4">
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
      <section className="w-full min-h-fit p-[1em] flex flex-col justify-between">
        <h3 className="m-0 text-3xl font-bold text-(--blue)">
          Asignación de Interfaces
        </h3>
        <p className="m-0 text-lg text-(--gray)">
          Seleccione interfaces con cambios para asignar a un usuario o asigne
          automáticamente todas las interfaces con cambios a los usuarios
          disponibles.
        </p>
        <div className="h-fit md:h-14 p-0 pt-4 flex flex-col gap-2 md:flex-row md:gap-0 md:justify-between">
          <div className="w-fit min-w-fit h-full flex flex-row flex-nowrap">
            <label
              htmlFor="assign"
              className="h-full m-0 py-2 px-2 flex items-center bg-(--blue) text-(--white) rounded-tl-lg rounded-bl-lg"
            >
              Buscar
            </label>
            <input
              type="text"
              className="bg-(--white) py-0 px-2 text-(--gray) border-t-[0.2em] border-r-[0.2em] border-b-[0.2em] border-solid border-(--gray-light) rounded-tr-lg rounded-br-lg"
              placeholder="Dato de la interfaz"
              onChange={(e) => {
                const filter = e.target.value;
                if (!filter) setViewAssignments(assignments);
                else
                  setViewAssignments(
                    OperationData.filterChangeInterfaces(assignments, filter)
                  );
              }}
            />
          </div>
          <form
            className="flex flex-row flex-nowrap gap-2"
            onSubmit={(e) => handlerSubmitUpdateStatus(e)}
          >
            <div className="w-fit h-[2.8rem] md:h-full flex flex-row flex-nowrap has-[select:disabled]:label:bg-(--gray) has-[select:disabled]:label:text-(--gray-light)">
              <label
                htmlFor="assign"
                className="h-full m-0 py-2 px-2 flex items-center bg-(--blue) text-(--white) rounded-tl-lg rounded-bl-lg"
              >
                Cambiar Estatus
              </label>
              <select
                className="min-w-2/6 h-full py-0 px-2 border-t-[0.2em] border-r-[0.2em] border-b-[0.2em] border-solid border-(--gray-light) bg-(--white) text-(--blue) text-lg rounded-tr-lg rounded-br-lg disabled:bg-(--gray-light) disabled:text-(--gray)"
                name="assing"
                id="assing"
                disabled={assignments.length <= 0}
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
              className="w-fit h-full py-2 px-4 flex items-center rounded-lg bg-(--blue) text-(--white) text-lg transition-all duration-300 ease-in-out cursor-pointer active:bg-(--blue-bright) hover:bg-(--blue-dark) disabled:bg-(--gray) disabled:text-(--gray-light) disabled:cursor-not-allowed"
              disabled={selectedInterfaces.length <= 0 || selectedStatus === ""}
            >
              Cambiar
            </button>
          </form>
        </div>
      </section>
      <section className="min-h-fit py-0 px-4">
        <InterfaceListComponent
          title="Interfaces con Cambios"
          interfaces={viewAssignments}
          onChange={(interfaces: InterfaceChangeSchema[]) =>
            setSelectedInterfaces(interfaces)
          }
        />
      </section>
    </main>
  );
}
