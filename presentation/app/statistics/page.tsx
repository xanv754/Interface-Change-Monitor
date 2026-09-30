"use client";

import NavbarComponent from "@/app/components/navbar/navbar";
import AlertModalComponent from "@/app/components/modal/alert";
import CardComponent from "@/app/components/card/main";
import Image from "next/image";
import { useState, useEffect } from "react";
import { SessionController } from "@/controllers/session";
import { StatisticsController } from "@/controllers/statistics";
import { InterfaceController } from "@/controllers/interfaces";
import { UserController } from "@/controllers/users";
import { StatusOption } from "@/app/components/card/main";
import { SessionSchema } from "@/schemas/user";
import { StatisticsAssignmentSchema } from "@/schemas/assignment";

export default function StatisticsPage() {
  const modalDefault = {
    showModal: true,
    title: "Cargando...",
    message: "Por favor, espere",
  };

  const [statistics, setStatistics] = useState<StatisticsAssignmentSchema[]>([]);
  const [totalChanges, setTotalChanges] = useState<number>(0);
  const [modal, setModal] = useState(modalDefault);
  const [user, setUser] = useState<SessionSchema | null>(null);

  const getTotalPending = () => {
    return statistics.reduce(
      (total, statistic) => total + statistic.total_pending_month,
      0
    );
  };

  const getTotalReviewed = () => {
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
      StatisticsController.getStatisticAllUsers(usernames).then((response) => {
        setStatistics(response);
      });
    });
    InterfaceController.getInterfaceChanges(1, 1).then((response) => {
      setTotalChanges(response.total);
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
        }}
      />
      <NavbarComponent user={user} />
      <div className="max-w-7xl mx-auto px-4 md:px-6 py-6 flex flex-col gap-6">
        <section className="w-full flex flex-row flex-wrap gap-4">
          <CardComponent
            title="Interfaces con Cambios Detectados"
            total={totalChanges}
            status={StatusOption.NORMAL}
          />
          <CardComponent
            title="Interfaces Pendientes por Revisión"
            total={getTotalPending()}
            status={StatusOption.PENDING}
          />
          <CardComponent
            title="Interfaces Revisadas"
            total={getTotalReviewed()}
            status={StatusOption.REVIEW}
          />
        </section>
        <section>
          <h1 className="font-display m-0 text-xl font-semibold text-(--ink)">
            Estadísticas de Usuarios
          </h1>
          <p className="m-0 mt-1 text-sm text-(--gray)">
            Revise las estadítiscas de asignaciones de los usuarios disponibles.
          </p>
        </section>
        <section className="flex flex-col gap-4">
          {statistics.length > 0 &&
            statistics.map(
              (statistic: StatisticsAssignmentSchema, index: number) => {
                return (
                  <div key={index} className="card w-full p-5 flex flex-col gap-4">
                    <div className="flex flex-row items-center gap-2">
                      <Image
                        src="/user/icon.svg"
                        alt="user"
                        width={20}
                        height={20}
                      />
                      <h3 className="font-display m-0 text-base font-semibold text-(--ink)">
                        {statistic.name} {statistic.lastname}
                      </h3>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-x-8 gap-y-4">
                      <div className="flex flex-col gap-0.5">
                        <span className="text-xs font-medium text-(--gray)">Asignadas en el día</span>
                        <span className="font-display text-lg font-semibold text-(--ink)">
                          {statistic.total_inspected_today +
                            statistic.total_rediscovered_today +
                            statistic.total_pending_today}
                        </span>
                      </div>
                      <div className="flex flex-col gap-0.5">
                        <span className="text-xs font-medium text-(--gray)">Pendientes en el día</span>
                        <span className="font-display text-lg font-semibold text-(--ink)">{statistic.total_pending_today}</span>
                      </div>
                      <div className="flex flex-col gap-0.5">
                        <span className="text-xs font-medium text-(--gray)">Revisadas en el día</span>
                        <span className="font-display text-lg font-semibold text-(--ink)">
                          {statistic.total_inspected_today + statistic.total_rediscovered_today}
                        </span>
                      </div>
                      <div className="flex flex-col gap-0.5">
                        <span className="text-xs font-medium text-(--gray)">Asignadas en el mes</span>
                        <span className="font-display text-lg font-semibold text-(--ink)">
                          {statistic.total_inspected_month +
                            statistic.total_rediscovered_month +
                            statistic.total_pending_month}
                        </span>
                      </div>
                      <div className="flex flex-col gap-0.5">
                        <span className="text-xs font-medium text-(--gray)">Pendientes en el mes</span>
                        <span className="font-display text-lg font-semibold text-(--ink)">{statistic.total_pending_month}</span>
                      </div>
                      <div className="flex flex-col gap-0.5">
                        <span className="text-xs font-medium text-(--gray)">Revisadas en el mes</span>
                        <span className="font-display text-lg font-semibold text-(--ink)">
                          {statistic.total_inspected_month + statistic.total_rediscovered_month}
                        </span>
                      </div>
                    </div>
                  </div>
                );
              }
            )}
          {statistics.length <= 0 && (
            <div className="card w-full p-8 flex flex-col justify-center items-center">
              <p className="m-0 text-sm text-(--gray)">
                No hay estadísticas disponibles.
              </p>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
