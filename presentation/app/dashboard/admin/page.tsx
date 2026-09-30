"use client";

import NavbarComponent from "@/app/components/navbar/navbar";
import CardComponent from "@/app/components/card/main";
import InterfaceListComponent from "@/app/components/list/interfaces";
import AlertModalComponent from "@/app/components/modal/alert";
import SelectUsersModalComponent from "@/app/components/modal/selectUsers";
import { useState, useEffect } from "react";
import { StatusOption } from "@/app/components/card/main";
import { InterfaceController } from "@/controllers/interfaces";
import { UserController } from "@/controllers/users";
import { AssignmentController } from "@/controllers/assignments";
import { StatisticsController } from "@/controllers/statistics";
import { SessionController } from "@/controllers/session";
import { InterfaceChangeSchema } from "@/schemas/interface";
import { UserSchema } from "@/schemas/user";
import { StatisticsAssignmentSchema } from "@/schemas/assignment";
import { SessionSchema } from "@/schemas/user";
import { OperationData } from "@/utils/operation";

export default function DashboardPage() {
  const modalDefault = {
    showModal: true,
    title: "Cargando...",
    message: "Por favor, espere",
  };

  const [interfaces, setChangeInterfaces] = useState<InterfaceChangeSchema[]>([]);
  const [viewInterfaces, setViewInterfaces] = useState<InterfaceChangeSchema[]>([]);
  const [totalChanges, setTotalChanges] = useState<number>(0);
  const [page, setPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [statistics, setStatistics] = useState<StatisticsAssignmentSchema[]>([]);
  const [selectedInterfaces, setSelectedInterfaces] = useState<InterfaceChangeSchema[]>([]);
  const [users, setUsers] = useState<UserSchema[]>([]);
  const [selectedUser, setSelectedUser] = useState<UserSchema | null>(null);
  const [assignAutomatic, setAssignAutomatic] = useState<boolean>(false);
  const [modal, setModal] = useState(modalDefault);
  const [user, setUser] = useState<SessionSchema | null>(null);

  const handlerSubmitAssignments = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();
    if (selectedInterfaces.length > 0 && selectedUser) {
      const statusResponse = await AssignmentController.newAssignments(
        selectedInterfaces, selectedUser.username
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

  const handlerAutomaticAssignment = async (users: UserSchema[]) => {
    if (users.length > 0) {
      const usernames = users.map((user) => user.username);
      const statusResponse = await AssignmentController.automaticAssignment(usernames);
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
  }

  const handlerGetTotalPendingStatistics = () => {
    return statistics.reduce(
      (total, statistic) => total + statistic.total_pending_month,
      0
    );
  };

  const handlerGetTotalReviewedStatistics = () => {
    return statistics.reduce(
      (total, statistic) =>
        total + statistic.total_inspected_month + statistic.total_rediscovered_month,
      0
    );
  };

  useEffect(() => {
    SessionController.getInfo().then((response) => {
      if (response) setUser(response);
      else SessionController.logout();
    });
    UserController.getAvailaibleAssignUsers().then((response) => {
      const usernames = response.map((user) => user.username);
      setUsers(response);
      StatisticsController.getStatisticAllUsers(usernames).then((response) => {
        setStatistics(response);
      });
    });
  }, []);

  useEffect(() => {
    InterfaceController.getInterfaceChanges(page).then((response) => {
      setChangeInterfaces(response.items);
      setViewInterfaces(response.items);
      setTotalChanges(response.total);
      setTotalPages(response.total_pages);
      setModal({ ...modalDefault, showModal: false });
    });
  }, [page]);

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
      {assignAutomatic && <SelectUsersModalComponent
        users={users}
        onAccept={(users: UserSchema[]) => {
          handlerAutomaticAssignment(users);
          setAssignAutomatic(false);
        }}
        onCancel={() => {
          setAssignAutomatic(false);
        }}
      />}
      <NavbarComponent user={user} />
      <div className="max-w-7xl mx-auto px-4 md:px-6 py-6 flex flex-col gap-6">
        <section className="w-full flex flex-row flex-wrap gap-4">
          <CardComponent
            title="Interfaces con Cambios Detectados Hoy"
            total={totalChanges}
            status={StatusOption.NORMAL}
          />
          <CardComponent
            title="Interfaces Pendientes en el Mes"
            total={handlerGetTotalPendingStatistics()}
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
                  if (!filter) setViewInterfaces(interfaces);
                  else
                    setViewInterfaces(
                      OperationData.filterChangeInterfaces(
                        interfaces,
                        filter
                      )
                    );
                }}
              />
            </div>
            <button
              className="btn btn-secondary"
              disabled={
                (!interfaces || interfaces.length <= 0) ||
                (!users || users.length <= 0)
              }
              onClick={() => { setAssignAutomatic(true) }}
            >
              Asignación Automática
            </button>
            <form
              className="flex flex-col sm:flex-row sm:items-end gap-3"
              onSubmit={(e) => handlerSubmitAssignments(e)}
            >
              <div className="w-full sm:w-56 flex flex-col gap-1.5">
                <label htmlFor="assing" className="text-sm font-medium text-(--ink)">
                  Asignar a
                </label>
                <select
                  className="field select"
                  name="assing"
                  id="assing"
                  disabled={
                    (!interfaces || interfaces.length <= 0) &&
                    (!users || users.length <= 0)
                  }
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
              <button
                type="submit"
                className="btn btn-primary"
                disabled={
                  !selectedInterfaces ||
                  selectedInterfaces.length <= 0 ||
                  !selectedUser
                }
              >
                Asignar
              </button>
            </form>
          </div>
        </section>
        <section className="flex flex-col gap-4">
          <InterfaceListComponent
            title="Interfaces con Cambios"
            interfaces={viewInterfaces}
            onChange={(interfaces: InterfaceChangeSchema[]) =>
              setSelectedInterfaces(interfaces)
            }
          />
          <div className="w-full flex flex-row justify-center items-center gap-4">
            <button
              className="btn btn-secondary"
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page <= 1}
            >
              Anterior
            </button>
            {totalPages > 0 && <p className="m-0 text-sm text-(--gray)">Página {page} de {totalPages}</p>}
            {totalPages <= 0 && <p className="m-0 text-sm text-(--gray)">Sin más contenido</p>}
            <button
              className="btn btn-secondary"
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page >= totalPages}
            >
              Siguiente
            </button>
          </div>
        </section>
      </div>
    </main>
  );
}
