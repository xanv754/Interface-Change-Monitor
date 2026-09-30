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
  }, [content.user, router]);

  return (
    <nav className="sticky top-0 z-20 w-full min-w-fit bg-(--white) border-b border-(--gray-light) py-3 px-4 flex flex-col lg:flex-row lg:items-center justify-between">
      <h1 className="font-display m-0 text-lg font-semibold text-(--ink) mb-4 lg:mb-0">
        Monitor de Cambios de Interfaces
      </h1>
      <ul className="m-0 p-0 flex flex-col md:flex-row gap-6 list-none items-start md:items-center">
        <li className="m-0">
          <a
            className="text-sm font-medium text-(--gray) no-underline border-b-2 border-transparent pb-1 transition-colors duration-150 hover:text-(--blue) hover:border-(--blue)"
            href={content.user && content.user.can_assign ? PATHS.DASHBOARD_ADMIN : PATHS.DASHBOARD_USER}
          >
            Inicio
          </a>
        </li>
        {content.user && content.user.can_assign && content.user.can_receive_assignment &&
          <li className="m-0">
            <a
              className="text-sm font-medium text-(--gray) no-underline border-b-2 border-transparent pb-1 transition-colors duration-150 hover:text-(--blue) hover:border-(--blue)"
              href={PATHS.DASHBOARD_USER}
            >
              Asignaciones
            </a>
          </li>
        }
        {content.user && content.user.can_assign && content.user.can_receive_assignment &&
          <li className="relative">
            <button
              id="dropAssignments"
              className="flex items-center gap-1.5 py-2 text-sm font-medium text-(--gray) cursor-pointer transition-colors duration-150 hover:text-(--blue)"
              onClick={() => {
                const dropAssignments = document.getElementById("dropAssignmentsOptions");
                if (dropAssignments) dropAssignments.classList.toggle("hidden");
              }}
            >
              Historial
              <Image
                src="/buttons/arrow.svg"
                alt="arrow"
                width={14}
                height={14}
              />
            </button>
            <div id="dropAssignmentsOptions" className="hidden absolute z-30 mt-1 font-normal bg-(--white) border border-(--gray-light) rounded-[var(--radius)] shadow-[var(--shadow-card)] w-48 overflow-hidden">
              <ul className="py-1 text-sm" aria-labelledby="dropdownLargeButton">
                <li>
                  <a href={PATHS.HISTORY_ADMIN} className="block px-4 py-2 text-(--ink) no-underline hover:bg-(--surface)">
                    Historial de Usuarios
                  </a>
                </li>
                <li>
                  <a href={PATHS.HISTORY_USER} className="block px-4 py-2 text-(--ink) no-underline hover:bg-(--surface)">
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
              className="text-sm font-medium text-(--gray) no-underline border-b-2 border-transparent pb-1 transition-colors duration-150 hover:text-(--blue) hover:border-(--blue)"
              href={content.user && content.user.can_assign ? PATHS.HISTORY_ADMIN : PATHS.HISTORY_USER}
            >
              Historial
            </a>
          </li>
        }
        {content.user && content.user.view_information_global &&
          <li className="m-0">
            <a className="text-sm font-medium text-(--gray) no-underline border-b-2 border-transparent pb-1 transition-colors duration-150 hover:text-(--blue) hover:border-(--blue)" href={PATHS.STATISTICS}>
              Estadísticas
            </a>
          </li>
        }
        {content.user &&
          (content.user.role === RoleTypes.ROOT ||
            content.user.role === RoleTypes.SOPORT) && (
            <li className="m-0">
              <a className="text-sm font-medium text-(--gray) no-underline border-b-2 border-transparent pb-1 transition-colors duration-150 hover:text-(--blue) hover:border-(--blue)" href={PATHS.SETTINGS}>
                Configuración
              </a>
            </li>
          )}
        <li className="relative">
          <button
            id="dropAccount"
            className="flex items-center gap-1.5 py-2 text-sm font-medium text-(--gray) cursor-pointer transition-colors duration-150 hover:text-(--blue)"
            onClick={() => {
              const dropAccount = document.getElementById("dropAccountOptions");
              if (dropAccount) dropAccount.classList.toggle("hidden");
            }}
          >
            Cuenta
            <Image
              src="/buttons/arrow.svg"
              alt="arrow"
              width={14}
              height={14}
            />
          </button>
          <div id="dropAccountOptions" className="right-0 hidden absolute z-30 mt-1 font-normal bg-(--white) border border-(--gray-light) divide-y divide-(--gray-light) rounded-[var(--radius)] shadow-[var(--shadow-card)] w-44 overflow-hidden">
            <a className="block w-full px-4 py-2.5 text-sm text-(--ink) no-underline cursor-pointer hover:bg-(--surface)" href={PATHS.PROFILE}>
              Perfil
            </a>
            <button
              className="block w-full text-left px-4 py-2.5 text-sm text-(--red) cursor-pointer hover:bg-(--red-light)"
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
