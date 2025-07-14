"use client";

import NavbarComponent from "../components/navbar/navbar";
import AlertModalComponent from "@/app/components/modal/alert";
import Image from "next/image";
import styles from './settings.module.css';
import { useState, useEffect } from "react";
import { SessionSchema } from "@/schemas/user";
import { ConfigurationSchema } from "@/schemas/configuration";
import { SessionController } from "@/controllers/session";


export default function SettingsPage() {
  const modalDefault = {
    showModal: true,
    title: "Cargando...",
    message: "Por favor, espere",
  };

  const [noEdit, setNoEdit] = useState(true);
  const [configOriginal, setConfigOriginal] = useState<ConfigurationSchema | null>(null);
  const [config, setConfig] = useState<ConfigurationSchema | null>(null);
  const [modal, setModal] = useState(modalDefault);
  const [user, setUser] = useState<SessionSchema | null>(null);

  const handlerSaveConfig = () => {
    if (!config) return;
    SessionController.updateConfiguration(config).then((response) => {
      if (response) {
        setConfigOriginal(config);
        setModal({
          showModal: true,
          title: "Configuración Guardada",
          message: "La configuración se ha guardado correctamente.",
        });
      } else {
        setModal({
          showModal: true,
          title: "Error al Guardar Configuración",
          message: "No se ha podido guardar la configuración.",
        });
      }
    });
  };

  const handlerEdit = () => {
    if (!noEdit) setConfig(configOriginal);
    setNoEdit(!noEdit);
  };

  useEffect(() => {
    SessionController.getInfo().then((response) => {
      if (response) setUser(response);
      else SessionController.logout();
    });
    SessionController.getConfigurationSystem().then((response) => {
      setConfig(response);
      setConfigOriginal(response);
      setModal({...modalDefault, showModal: false});
    });
  }, []);

  return (
    <main className="w-full h-fit">
      <NavbarComponent user={user} />
      <AlertModalComponent
        showModal={modal.showModal}
        title={modal.title}
        message={modal.message}
        onClick={() => {
          setModal(modalDefault);
          window.location.reload();
        }}
      />
      <div className="w-full p-4 flex flex-col flex-nowrap gap-4">
        <section className="w-full flex flex-row justify-end gap-2">
          {noEdit && <p className="font-semibold text-(--gray) cursor-default">Habilitar Edición de Configuración</p>}
          {!noEdit && <p className="font-semibold text-(--gray) cursor-default">Deshabilitar Edición de Configuración</p>}
          <button
            onClick={() => { handlerEdit(); }}
            className="w-fit h-fit cursor-pointer"
          >
            <Image
              src="/buttons/edit.svg"
              alt="edit"
              width={24}
              height={24}
            />
          </button>
        </section>
        <section className="w-full p-4 flex flex-col flex-nowrap bg-(--white) border-[0.2em] border-solid border-(--gray-light) rounded-lg shadow-[0.2em_0.3em_0.5em_rgba(0,0,0,0.2)]">
          <h1 className="pb-4 m-0 text-2xl font-semibold text-(--blue)">Notificaciones de Cambios</h1>
          <div id="notifications" className="flex flex-row flex-nowrap items-center gap-10">
            <div className="m-0 text-lg font-normal text-(--gray) w-fit flex flex-col gap-4">
              <h3 id="notification-option">Notificar Cambios en el Campo "ifName"</h3>
              <h3 id="notification-option">Notificar Cambios en el Campo "ifDescr"</h3>
              <h3 id="notification-option">Notificar Cambios en el Campo "ifAlias"</h3>
            </div>
            <div className={`w-fit flex flex-col gap-4`}>
              <label id="notification-ifname-option" className={`${styles.switch}`}>
                <input
                  type="checkbox"
                  onClick={() => {
                    if (config) {
                      setConfig({
                        ...config,
                        notification_changes: {
                          ...config.notification_changes,
                          ifName: !config.notification_changes.ifName
                        }
                      });
                    }
                  }}
                  disabled={noEdit}
                />
                <span className={`${styles.slider} ${config?.notification_changes?.ifName ? styles.active : ""}`}></span>
              </label>
              <label id="notification-ifdescr-option" className={`${styles.switch}`}>
                <input
                  type="checkbox"
                  onClick={() => {
                    if (config) {
                      setConfig({
                        ...config,
                        notification_changes: {
                          ...config.notification_changes,
                          ifDescr: !config.notification_changes.ifDescr
                        }
                      });
                    }
                  }}
                  disabled={noEdit}
                />
                <span className={`${styles.slider} ${config?.notification_changes?.ifDescr ? styles.active : ""}`}></span>
              </label>
              <label id="notification-ifalias-option" className={`${styles.switch}`}>
                <input
                  type="checkbox"
                  onClick={() => {
                    if (config) {
                      setConfig({
                        ...config,
                        notification_changes: {
                          ...config.notification_changes,
                          ifAlias: !config.notification_changes.ifAlias
                        }
                      });
                    }
                  }}
                  disabled={noEdit}
                />
                <span className={`${styles.slider} ${config?.notification_changes?.ifAlias ? styles.active : ""}`}></span>
              </label>
            </div>
            <div className="m-0 text-lg font-normal text-(--gray) w-fit flex flex-col gap-4">
              <h3 id="notification-option">Notificar Cambios en el Campo "ifHighSpeed"</h3>
              <h3 id="notification-option">Notificar Cambios en el Campo "ifOperStatus"</h3>
              <h3 id="notification-option">Notificar Cambios en el Campo "ifAdminStatus"</h3>
            </div>
            <div className={`w-fit flex flex-col gap-4`}>
              <label id="notification-ifhighspeed-option" className={`${styles.switch}`}>
                <input
                  type="checkbox"
                  onClick={() => {
                    if (config) {
                      setConfig({
                        ...config,
                        notification_changes: {
                          ...config.notification_changes,
                          ifHighSpeed: !config.notification_changes.ifHighSpeed
                        }
                      });
                    }
                  }}
                  disabled={noEdit}
                />
                <span className={`${styles.slider} ${config?.notification_changes?.ifHighSpeed ? styles.active : ""}`}></span>
              </label>
              <label id="notification-ifoperstatus-option" className={`${styles.switch}`}>
                <input
                  type="checkbox"
                  onClick={() => {
                    if (config) {
                      setConfig({
                        ...config,
                        notification_changes: {
                          ...config.notification_changes,
                          ifOperStatus: !config.notification_changes.ifOperStatus
                        }
                      });
                    }
                  }}
                  disabled={noEdit}
                />
                <span className={`${styles.slider} ${config?.notification_changes?.ifOperStatus ? styles.active : ""}`}></span>
              </label>
              <label id="notification-ifadminstatus-option" className={`${styles.switch}`}>
                <input
                  type="checkbox"
                  onClick={() => {
                    if (config) {
                      setConfig({
                        ...config,
                        notification_changes: {
                          ...config.notification_changes,
                          ifAdminStatus: !config.notification_changes.ifAdminStatus
                        }
                      });
                    }
                  }}
                  disabled={noEdit}
                />
                <span className={`${styles.slider} ${config?.notification_changes?.ifAdminStatus ? styles.active : ""}`}></span>
              </label>
            </div>
          </div>
        </section>
        <section className="w-full p-4 flex flex-col flex-nowrap bg-(--white) border-[0.2em] border-solid border-(--gray-light) rounded-lg shadow-[0.2em_0.3em_0.5em_rgba(0,0,0,0.2)]">
          <h1 className="pb-4 m-0 text-2xl font-semibold text-(--blue)">Permisos de Administradores</h1>
          <div id="notifications" className="flex flex-row flex-nowrap items-center gap-10">
            <div className="m-0 text-lg font-normal text-(--gray) w-fit flex flex-col gap-4">
              <h3 id="notification-option">Los administradores pueden asignar interfaces</h3>
              <h3 id="notification-option">Los administradores pueden recibir asignaciones de interfaces</h3>
              <h3 id="notification-option">Los administradores pueden revisar todas las estadísticas</h3>
              {/* <h3 id="notification-option">Los administradores pueden cambiar las configuraciones del sistema</h3> */}
            </div>
            <div className={`w-fit flex flex-col gap-4`}>
              <label id="admin-assign-option" className={`${styles.switch}`}>
                <input
                  type="checkbox"
                  onClick={() => {
                    if (config) {
                      setConfig({
                        ...config,
                        can_assign: {
                          ...config.can_assign,
                          admin: !config.can_assign.admin
                        }
                      });
                    }
                  }}
                  disabled={noEdit}
                />
                <span className={`${styles.slider} ${config?.can_assign?.admin ? styles.active : ""}`}></span>
              </label>
              <label id="admin-receive-assignment-option" className={`${styles.switch}`}>
                <input
                  type="checkbox"
                  onClick={() => {
                    if (config) {
                      setConfig({
                        ...config,
                        can_receive_assignment: {
                          ...config.can_receive_assignment,
                          admin: !config.can_receive_assignment.admin
                        }
                      });
                    }
                  }}
                  disabled={noEdit}
                />
                <span className={`${styles.slider} ${config?.can_receive_assignment?.admin ? styles.active : ""}`}></span>
              </label>
              <label id="admin-view-global-option" className={`${styles.switch}`}>
                <input
                  type="checkbox"
                  onClick={() => {
                    if (config) {
                      setConfig({
                        ...config,
                        view_information_global: {
                          ...config.view_information_global,
                          admin: !config.view_information_global.admin
                        }
                      });
                    }
                  }}
                  disabled={noEdit}
                />
                <span className={`${styles.slider} ${config?.view_information_global?.admin ? styles.active : ""}`}></span>
              </label>
              {/* <label id="admin-view-information-option" className={`${styles.switch}`}>
                <input 
                  type="checkbox"
                  checked={config?.view_information_global?.admin ?? false}
                  disabled={noEdit}
                />
                <span className={`${styles.slider}`}></span>
              </label> */}
            </div>
          </div>
        </section>
        <section className="w-full flex flex-row justify-center">
          <button
            className="w-fit h-full py-2 px-4 flex items-center rounded-lg bg-(--blue) text-(--white) transition-all duration-300 ease-in-out cursor-pointer active:bg-(--blue-bright) hover:bg-(--blue-dark) disabled:bg-(--gray) disabled:text-(--gray-light) disabled:cursor-not-allowed"
            onClick={() => { handlerSaveConfig(); }}
            disabled={noEdit}
          >
            Guardar Configuración
          </button>
        </section>
      </div>
    </main>
  );
}
