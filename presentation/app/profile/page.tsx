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
  const [userOriginal, setUserOriginal] = useState<SessionSchema | null>(null);
  const [newPassword, setNewPassword] = useState<PasswordSchema | null>(null);
  const [save, setSave] = useState(true);

  const handlerEdit = () => {
    setNotEdit(!notEdit);
  };

  const activeModal = (status: boolean) => {
    if (status) {
      setModal({
        showModal: true,
        title: "Datos de Personales Actualizados",
        message: "Los datos de personales se han actualizado correctamente.",
      });
    } else {
      setModal({
        showModal: true,
        title: "Error al Actualizar Datos de Personales",
        message: "No se han podido actualizar todos los datos ingresados.",
      });
    }
  }

  const validatePassword = () => {
    if (newPassword && newPassword.password && newPassword.confirm)
      return newPassword.password === newPassword.confirm;
    return false;
  }

  const hasDifferentUser = () => {
    if (user && userOriginal)
      return user.name != userOriginal.name || user.lastname != userOriginal.lastname;
    return false;
  }

  const updateUser = () => {
    const response = SessionController.updateInfo(user!).then((response) => {
      if (response) return true;
      else return false;
    });
    return response;
  }

  const updatePassword = () => {
    const response = SessionController.updatePassword(newPassword!.password).then((response) => {
      if (response) return true;
      else return false;
    });
    return response;
  }

  const handlerSaveUser = async () => {
    if (!user || !userOriginal) return;
    const isValid = validatePassword();
    const differentUser = hasDifferentUser();
    if (differentUser && !isValid) {
      const response = await updateUser();
      if (response) activeModal(true);
      else activeModal(false);
    }
    else if (!differentUser && isValid) {
      const response = await updatePassword();
      if (response) activeModal(true);
      else activeModal(false);
    }
    else if (differentUser && isValid) {
      const userResponse = await updateUser();
      const passwordResponse = await updatePassword();
      if (userResponse && passwordResponse) activeModal(true);
      if (!userResponse) activeModal(false);
    }
  };

  useEffect(() => {
    SessionController.getInfo().then((response) => {
      if (response) {
        setUser(response);
        setUserOriginal(response);
      }
      else SessionController.logout();
    });
  }, []);

  useEffect(() => {
    const isValid = validatePassword();
    const differentUser = hasDifferentUser();
    if (differentUser || isValid) setSave(false);
    else setSave(true);
  }, [user, newPassword]);

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
          <h1 className="m-0 py-0 px-1 text-3xl font-semibold text-(--blue)">Datos de Personales</h1>
          <button
            onClick={() => { 
              handlerEdit(); 
              setNewPassword(null);
            }}
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
        <section className="w-full p-4 flex flex-col flex-nowrap bg-(--white) border-[0.2em] border-solid border-(--gray-light) rounded-lg shadow-[0.2em_0.3em_0.5em_rgba(0,0,0,0.2)] gap-2">
          <div className="flex flex-col">
            <Image
              src="/user/alternative.svg"
              alt="user"
              width={128}
              height={128}
            />
            <h2 className="m-0 text-xl font-bold text-(--blue)">{user?.username}</h2>
          </div>
          <div className="flex flex-row flex-nowrap gap-10">
            <section className="flex flex-col flex-nowrap gap-2">
              <div className="w-fit h-fit flex flex-col justify-center">
                <label htmlFor="name" className="m-0 text-lg font-medium text-(--blue)">Nombre</label>
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
                    } else if (!value && user && userOriginal) {
                      setUser({
                        ...user,
                        name: userOriginal?.name
                      });
                    }
                  }}
                  disabled={notEdit}
                />
              </div>
              <div className="w-fit h-fit flex flex-col justify-center">
                <label htmlFor="lastname" className="m-0 text-lg font-medium text-(--blue)">Apellido</label>
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
                    } else if (!value && user && userOriginal) {
                      setUser({
                        ...user,
                        lastname: userOriginal?.lastname
                      });
                    }
                  }}
                  disabled={notEdit}
                />
              </div>
              <div className="w-fit h-fit flex flex-col justify-center">
                <label htmlFor="lastname" className="m-0 text-lg font-medium text-(--blue)">Nueva Contraseña</label>
                <input
                  type="text"
                  id="lastname"
                  className={styles.fieldInput}
                  placeholder="Nueva contraseña"
                  onChange={(e) => {
                    let value = e.target.value;
                    if (!value && newPassword) {
                      setNewPassword({
                        ...newPassword,
                        password: ""
                      });
                    }
                    else if (value && !newPassword) {
                      setNewPassword({
                        password: value,
                        confirm: ""
                      });
                    } else if (newPassword) {
                      setNewPassword({
                        ...newPassword,
                        password: value
                      });
                    }
                  }}
                  disabled={notEdit}
                />
              </div>
            </section>
            <section className="flex flex-col flex-nowrap gap-2">
              <div className="w-fit h-fit flex flex-col justify-center">
                <label htmlFor="rol" className="m-0 text-lg font-medium text-(--blue)">Rol</label>
                <input type="text" id="rol" className={styles.fieldInput} placeholder={user?.role} disabled />
              </div>
              <div className="w-fit h-fit flex flex-col justify-center">
                <label htmlFor="status" className="m-0 text-lg font-medium text-(--blue)">Estatus</label>
                <input type="text" id="status" className={styles.fieldInput} placeholder={user?.status} disabled />
              </div>
              <div className="w-fit h-fit flex flex-col justify-center">
                <label htmlFor="lastname" className="m-0 text-lg font-medium text-(--blue)">Confirmar Contraseña</label>
                <input
                  type="text"
                  id="lastname"
                  className={styles.fieldInput}
                  placeholder="Confirmar contraseña"
                  onChange={(e) => {
                    let value = e.target.value;
                    if (!value && newPassword) {
                      setNewPassword({
                        ...newPassword,
                        confirm: ""
                      });
                    }
                    else if (value && !newPassword) {
                      setNewPassword({
                        password: "",
                        confirm: value
                      });
                    } else if (newPassword) {
                      setNewPassword({
                        ...newPassword,
                        confirm: value
                      });
                    }
                  }}
                  disabled={notEdit}
                />
                <span className={`text-xs text-(--red) ${(!newPassword || validatePassword()) ? 'hidden' : 'visible'}`}>* Contraseñas deben coincidir</span>
              </div>
            </section>
          </div>
        </section>
        <section className="w-full mt-4 flex flex-row justify-center">
          <button
            onClick={() => { handlerSaveUser(); }}
            className="w-fit h-full py-2 px-4 flex items-center rounded-lg bg-(--blue) text-(--white) transition-all duration-300 ease-in-out cursor-pointer active:bg-(--blue-bright) hover:bg-(--blue-dark) disabled:bg-(--gray) disabled:text-(--gray-light) disabled:cursor-not-allowed"
            disabled={save}
          >
            Guardar Configuración
          </button>
        </section>
      </div>
    </main>
  );
}