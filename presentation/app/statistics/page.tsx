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
import { InterfaceChangeSchema } from "@/schemas/interface";

export default function StatisticsPage() {
  const modalDefault = {
    showModal: false,
    title: "Cargando...",
    message: "Por favor, espere",
  };

  const [statistics, setStatistics] = useState<StatisticsAssignmentSchema[]>([]);
  const [interfaces, setInterfaces] = useState<InterfaceChangeSchema[]>([]);
  const [modal, setModal] = useState(modalDefault);
  const [user, setUser] = useState<SessionSchema | null>(null);

  const getTotalPending = () => {
    let total = 0;
    statistics.map((statistic: StatisticsAssignmentSchema) => {
      total += statistic.total_pending_month;
    });
    return total;
  };

  const getTotalReviewed = () => {
    let total = 0;
    statistics.map((statistic: StatisticsAssignmentSchema) => {
      total += statistic.total_inspected_month;
      total += statistic.total_rediscovered_month;
    });
    return total;
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
    InterfaceController.getInterfaceChanges().then((response) => {
      setInterfaces(response);
    });
  }, []);

  return (
    <main>
      <AlertModalComponent
        showModal={modal.showModal}
        title={modal.title}
        message={modal.message}
        onClick={() => {
          setModal(modalDefault);
        }}
      />
      <NavbarComponent user={user} />
      <section
        id="statistics-general"
        className="w-full py-2 px-4 flex flex-row flex-nowrap gap-4"
      >
        <CardComponent
          title="Interfaces con Cambios Detectados"
          total={interfaces.length ?? 0}
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
      <section
        id="description"
        className="w-full px-4 flex flex-col flex-nowrap"
      >
        <h1 className="text-(--blue) text-3xl font-bold">
          Estadísticas de Usuarios
        </h1>
        <p className="text-(--gray) text-lg">
          Revise las estadítiscas de asignaciones de los usuarios disponibles.
        </p>
      </section>
      {statistics &&
        statistics.length > 0 &&
        statistics.map(
          (statistic: StatisticsAssignmentSchema, index: number) => {
            return (
              <section
                key={index}
                id="statistics-user"
                className="w-full pb-4 px-4 flex flex-col flex-nowrap gap-4"
              >
                <div className="w-full px-4 flex flex-col flex-nowrap bg-(--white) border-[0.2em] border-solid border-(--gray-light) rounded-lg shadow-[0.2em_0.3em_0.5em_rgba(0,0,0,0.2)]">
                  <section
                    id="title"
                    className="w-full p-2 flex flex-row gap-2"
                  >
                    <Image
                      src="/user/icon.svg"
                      alt="user"
                      width={24}
                      height={24}
                    />
                    <h3 className="text-xl font-bold text-(--blue)">
                      {statistic.name} {statistic.lastname}
                    </h3>
                  </section>
                  <section
                    id="content"
                    className="w-full flex flex-row flex-nowrap gap-20"
                  >
                    <div className="flex flex-col flex-nowrap">
                      <div className="w-fit h-fit flex flex-col flex-nowrap">
                        <h3 className="text-(--gray) font-bold text-lg">
                          Interfaces Asignadas en el día
                        </h3>
                        <p className="text-(--gray) text-lg">
                          {statistic.total_inspected_today + 
                            statistic.total_rediscovered_today +
                            statistic.total_pending_today
                          }
                        </p>
                      </div>
                      <div className="w-fit h-fit flex flex-col flex-nowrap">
                        <h3 className="text-(--gray) font-bold text-lg">
                          Interfaces Asignadas en el Mes
                        </h3>
                        <p className="text-(--gray) text-lg">
                          {statistic.total_inspected_month + 
                            statistic.total_rediscovered_month +
                            statistic.total_pending_month
                          }
                        </p>
                      </div>
                    </div>
                    <div className="flex flex-col flex-nowrap">
                      <div className="w-fit h-fit flex flex-col flex-nowrap">
                        <h3 className="text-(--gray) font-bold text-lg">
                          Interfaces Pendientes en el día
                        </h3>
                        <p className="text-(--gray) text-lg">{statistic.total_pending_today}</p>
                      </div>
                      <div className="w-fit h-fit flex flex-col flex-nowrap">
                        <h3 className="text-(--gray) font-bold text-lg">
                          Interfaces Pendientes en el Mes
                        </h3>
                        <p className="text-(--gray) text-lg">{statistic.total_pending_month}</p>
                      </div>
                    </div>
                    <div className="flex flex-col flex-nowrap">
                      <div className="w-fit h-fit flex flex-col flex-nowrap">
                        <h3 className="text-(--gray) font-bold text-lg">
                          Interfaces Revisadas en el día
                        </h3>
                        <p className="text-(--gray) text-lg">
                          {statistic.total_inspected_today + 
                            statistic.total_rediscovered_today
                          }
                        </p>
                      </div>
                      <div className="w-fit h-fit flex flex-col flex-nowrap">
                        <h3 className="text-(--gray) font-bold text-lg">
                          Interfaces Revisadas en el Mes
                        </h3>
                        <p className="text-(--gray) text-lg">
                          {statistic.total_inspected_month + 
                            statistic.total_rediscovered_month
                          }
                        </p>
                      </div>
                    </div>
                  </section>
                </div>
              </section>
            );
          }
        )}
    </main>
  );
}
