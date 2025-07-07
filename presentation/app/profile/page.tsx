"use client";

import NavbarComponent from "../components/navbar/navbar";
import AlertModalComponent from "@/app/components/modal/alert";
import Image from "next/image";
import styles from './profile.module.css';
import { useState, useEffect } from "react";
import { SessionSchema } from "@/schemas/user";
import { SessionController } from "@/controllers/session";

interface PasswordSchema {
  password: string;
  confirm: string;
}

export default function ProfilePage() {
  const modalDefault = {
    showModal: false,
    title: "Cargando...",
    message: "Por favor, espere",
  };

  const [modal, setModal] = useState(modalDefault);
  const [notEdit, setNotEdit] = useState(true);
  const [user, setUser] = useState<SessionSchema | null>(null);
  const [newPassword, setNewPassword] = useState<PasswordSchema | null>(null);

  const handlerEdit = () => {
    setNotEdit(!notEdit);
  };

  const handlerSaveUser = () => {
    if (!user) return;
    SessionController.updateInfo(user).then((response) => {
      if (response) {
        setModal({
          showModal: true,
          title: "Datos de Personales Guardados",
          message: "Los datos de personales se han guardado correctamente.",
        });
      } else {
        setModal({
          showModal: true,
          title: "Error al Guardar Datos de Personales",
          message: "No se han podido guardar los datos de personales.",
        });
      }
    });
  };

  useEffect(() => {
    SessionController.getInfo().then((response) => {
      if (response) setUser(response);
      else SessionController.logout();
    });
  }, []);

  return (
    <main>
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
      <div className="w-full p-4 flex flex-col flex-nowrap gap-2">
        <section className="w-full flex flex-row justify-between items-center">
          <h1 className={styles.title}>Datos de Personales</h1>
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
        <section className={styles.sectionSetting}>
          <div className="flex flex-col">
            <Image
              src="/user/alternative.svg"
              alt="user"
              width={128}
              height={128}
            />
            <h2>{user?.username}</h2>
          </div>
          <div className="flex flex-row flex-nowrap gap-10">
            <section className="flex flex-col flex-nowrap gap-2">
              <div className="w-fit h-fit flex flex-col justify-center">
                <label htmlFor="name" className={styles.fieldLabel}>Nombre</label>
                <input 
                  type="text" 
                  id="name" 
                  className={styles.fieldInput} 
                  placeholder={user?.name} 
                  onChange={(e) => {
                    let value = e.target.value;
                    if (value && user) {  
                      setUser({
                        ...user,
                        name: e.target.value
                      });
                    }
                  }}
                  disabled={notEdit} 
                />
              </div>
              <div className="w-fit h-fit flex flex-col justify-center">
                <label htmlFor="lastname" className={styles.fieldLabel}>Apellido</label>
                <input 
                  type="text" 
                  id="lastname" 
                  className={styles.fieldInput} 
                  placeholder={user?.lastname} 
                  onChange={(e) => {
                    let value = e.target.value;
                    if (value && user) {  
                      setUser({
                        ...user,
                        lastname: e.target.value
                      });
                    }
                  }}
                  disabled={notEdit} />
              </div>
            </section>
            <section className="flex flex-col flex-nowrap gap-2">
              <div className="w-fit h-fit flex flex-col justify-center">
                <label htmlFor="rol" className={styles.fieldLabel}>Rol</label>
                <input type="text" id="rol" className={styles.fieldInput} placeholder={user?.role} disabled />
              </div>
              <div className="w-fit h-fit flex flex-col justify-center">
                <label htmlFor="status" className={styles.fieldLabel}>Estatus</label>
                <input type="text" id="status" className={styles.fieldInput} placeholder={user?.status} disabled />
              </div>
            </section>
          </div>
        </section>
        <section className="w-full mt-4 flex flex-row justify-center">
          <button
            onClick={() => { handlerSaveUser(); }}
            className={styles.btn}
            disabled={notEdit}
          >
            Guardar Configuración
          </button>
        </section>
      </div>
    </main>
  );
}