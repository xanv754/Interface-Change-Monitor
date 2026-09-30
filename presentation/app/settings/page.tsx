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
    <main className="w-full min-h-screen">
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
      <div className="max-w-7xl mx-auto px-4 md:px-6 py-6 flex flex-col gap-4">
        <section className="w-full flex flex-row justify-end items-center gap-2">
          {noEdit && <p className="m-0 text-sm font-medium text-(--gray) cursor-default">Habilitar Edición de Configuración</p>}
          {!noEdit && <p className="m-0 text-sm font-medium text-(--gray) cursor-default">Deshabilitar Edición de Configuración</p>}
          <button
            onClick={() => { handlerEdit(); }}
            className="w-fit h-fit p-2 rounded-[var(--radius)] cursor-pointer hover:bg-(--surface)"
          >
            <Image
              src="/buttons/edit.svg"
              alt="edit"
              width={20}
              height={20}
            />
          </button>
        </section>
        <section className="card w-full p-5 flex flex-col flex-nowrap gap-5">
          <h1 className="font-display m-0 text-xl font-semibold text-(--ink)">Notificaciones de Cambios</h1>
          <div className="flex flex-row flex-wrap items-start gap-x-12 gap-y-6">
            <div className="text-sm font-normal text-(--ink) w-fit flex flex-col gap-4">
              <h3 className="m-0 font-normal">Notificar Cambios en el Campo &quot;ifName&quot;</h3>
              <h3 className="m-0 font-normal">Notificar Cambios en el Campo &quot;ifDescr&quot;</h3>
              <h3 className="m-0 font-normal">Notificar Cambios en el Campo &quot;ifAlias&quot;</h3>
            </div>
            <div className="w-fit flex flex-col gap-4">
              <label className={`${styles.switch}`}>
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
              <label className={`${styles.switch}`}>
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
              <label className={`${styles.switch}`}>
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
            <div className="text-sm font-normal text-(--ink) w-fit flex flex-col gap-4">
              <h3 className="m-0 font-normal">Notificar Cambios en el Campo &quot;ifHighSpeed&quot;</h3>
              <h3 className="m-0 font-normal">Notificar Cambios en el Campo &quot;ifOperStatus&quot;</h3>
              <h3 className="m-0 font-normal">Notificar Cambios en el Campo &quot;ifAdminStatus&quot;</h3>
            </div>
            <div className="w-fit flex flex-col gap-4">
              <label className={`${styles.switch}`}>
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
              <label className={`${styles.switch}`}>
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
              <label className={`${styles.switch}`}>
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
        <section className="card w-full p-5 flex flex-col flex-nowrap gap-5">
          <h1 className="font-display m-0 text-xl font-semibold text-(--ink)">Permisos de Administradores</h1>
          <div className="flex flex-row flex-wrap items-start gap-x-12 gap-y-6">
            <div className="text-sm font-normal text-(--ink) w-fit flex flex-col gap-4">
              <h3 className="m-0 font-normal">Los administradores pueden asignar interfaces</h3>
              <h3 className="m-0 font-normal">Los administradores pueden recibir asignaciones de interfaces</h3>
              <h3 className="m-0 font-normal">Los administradores pueden revisar todas las estadísticas</h3>
              {/* <h3>Los administradores pueden cambiar las configuraciones del sistema</h3> */}
            </div>
            <div className="w-fit flex flex-col gap-4">
              <label className={`${styles.switch}`}>
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
              <label className={`${styles.switch}`}>
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
              <label className={`${styles.switch}`}>
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
              {/* <label className={`${styles.switch}`}>
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
            className="btn btn-primary"
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
