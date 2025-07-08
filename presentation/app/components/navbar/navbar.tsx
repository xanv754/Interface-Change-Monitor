"use client";

import Image from "next/image";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { PATHS } from "@/constants/paths";
import { RoleTypes } from "@/constants/types";
import { SessionSchema } from "@/schemas/user";
import { SessionController } from "@/controllers/session";

/**
 * Component to show the navbar.
 *
 * @param user - User session.
 */
interface NavbarProps {
  user: SessionSchema | null;
}

export default function NavbarComponent(content: NavbarProps) {
  const router = useRouter();

  const handlerLogout = () => {
    SessionController.logout();
    router.push(PATHS.LOGIN);
  };

  useEffect(() => {
    if (
      content.user &&
      !content.user.can_assign &&
      !content.user.can_receive_assignment
    ) {
      router.push(PATHS.LOBBY);
    }
  }, []);

  return (
    <nav className="w-full min-w-fit bg-(--blue) py-3 px-4 flex flex-col lg:flex-row justify-between">
      <h1 className="m-0 text-2xl font-bold text-(--white) mb-4 lg:mb-0">
        Monitor de Cambios de Interfaces
      </h1>
      <ul className="m-0 p-0 flex flex-col md:flex-row gap-6 list-none items-center">
        <li className="m-0">
          <a
            className="text-(--white) no-underline transition-all duration-300 ease-in-out hover:text-(--yellow)"
            href={content.user && content.user.can_assign ? PATHS.DASHBOARD_ADMIN : PATHS.DASHBOARD_USER}
          >
            Inicio
          </a>
        </li>
        {content.user && content.user.can_assign && content.user.can_receive_assignment &&
          <li className="m-0">
            <a
              className="text-(--white) no-underline transition-all duration-300 ease-in-out hover:text-(--yellow)"
              href={PATHS.DASHBOARD_USER}
            >
              Asignaciones
            </a>
          </li>
        }
        {content.user && content.user.can_assign && content.user.can_receive_assignment &&
          <li>
            <button
              id="dropAssignments"
              className="flex items-center justify-between w-full py-2 px-3 text-(--white)"
              onClick={() => {
                const dropAssignments = document.getElementById("dropAssignmentsOptions");
                if (dropAssignments) dropAssignments.classList.toggle("hidden");
              }}
            >
              Historial
              <Image
                src="/buttons/arrow.svg"
                alt="arrow"
                width={18}
                height={18}
              />
            </button>
            <div id="dropAssignmentsOptions" className="hidden absolute font-normal bg-(--blue-dark) rounded-lg shadow-sm w-44">
              <ul className="py-4 text-sm" aria-labelledby="dropdownLargeButton">
                <li>
                  <a href={PATHS.HISTORY_ADMIN} className="block px-4 py-2 text-(--white)">
                    Historial de Usuarios
                  </a>
                </li>
                <li>
                  <a href={PATHS.HISTORY_USER} className="block px-4 py-2 text-(--white)">
                    Mi historial
                  </a>
                </li>
              </ul>
            </div>
          </li>
        }
        {content.user && (!content.user.can_assign || !content.user.can_receive_assignment) &&
          <li className="m-0">
            <a
              className="text-(--white) no-underline transition-all duration-300 ease-in-out hover:text-(--yellow)"
              href={content.user && content.user.can_assign ? PATHS.HISTORY_ADMIN : PATHS.HISTORY_USER}
            >
              Historial
            </a>
          </li>
        }
        {content.user && content.user.view_information_global &&
          <li className="m-0">
            <a className="text-(--white)" href={PATHS.STATISTICS}>
              Estadísticas
            </a>
          </li>
        }
        {content.user &&
          (content.user.role === RoleTypes.ROOT ||
            content.user.role === RoleTypes.SOPORT) && (
            <li className="m-0">
              <a className="text-(--white)" href={PATHS.SETTINGS}>
                Configuración
              </a>
            </li>
          )}
        <li>
          <button
            id="dropAccount"
            className="flex items-center justify-between w-full py-2 text-(--white)"
            onClick={() => {
              const dropAccount = document.getElementById("dropAccountOptions");
              if (dropAccount) dropAccount.classList.toggle("hidden");
            }}
          >
            Cuenta
            <Image
              src="/buttons/arrow.svg"
              alt="arrow"
              width={18}
              height={18}
            />
          </button>
          <div id="dropAccountOptions" className="right-2 hidden absolute font-normal bg-(--blue-dark) divide-y divide-gray-100 rounded-lg shadow-sm w-44">
            <div className="m-0 p-4">
              <a className="w-full text-(--white) text-sm cursor-pointer" href={PATHS.PROFILE}>
                Perfil
              </a>
            </div>
            <button
              className="p-4 text-(--white) text-sm cursor-pointer"
              onClick={() => {
                handlerLogout();
              }}
            >
              Cerrar Sesión
            </button>
          </div>
        </li>
      </ul>
    </nav>
  );
}
