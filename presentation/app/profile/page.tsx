"use client";

import NavbarComponent from "../components/navbar/navbar";
import AlertModalComponent from "@/app/components/modal/alert";
import Image from "next/image";
import { useState, useEffect } from "react";
import { SessionSchema } from "@/schemas/user";
import { SessionController } from "@/controllers/session";

interface PasswordSchema {
  password: string;
  confirm: string;
}

export default function ProfilePage() {
  const modalDefault = {
    showModal: true,
    title: "Cargando...",
    message: "Por favor, espere",
  };

  const [modal, setModal] = useState(modalDefault);
  const [noEdit, setNoEdit] = useState(true);
  const [user, setUser] = useState<SessionSchema | null>(null);
  const [userOriginal, setUserOriginal] = useState<SessionSchema | null>(null);
  const [newPassword, setNewPassword] = useState<PasswordSchema | null>(null);
  const [save, setSave] = useState(true);

  const handlerEdit = () => {
    setNoEdit(!noEdit);
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
      else activeModal(false);
    }
  };

  useEffect(() => {
    SessionController.getInfo().then((response) => {
      setModal({...modalDefault, showModal: false});
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
        <section className="w-full flex flex-row justify-between items-center">
          <h1 className="font-display m-0 text-xl font-semibold text-(--ink)">Datos de Personales</h1>
          <button
            onClick={() => {
              handlerEdit();
              setNewPassword(null);
            }}
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
          <div className="flex flex-col items-start gap-2">
            <Image
              src="/user/alternative.svg"
              alt="user"
              width={96}
              height={96}
            />
            <h2 className="font-display m-0 text-lg font-semibold text-(--ink)">{user?.username}</h2>
          </div>
          <div className="flex flex-col sm:flex-row flex-wrap gap-x-10 gap-y-4">
            <section className="flex flex-col flex-nowrap gap-4 w-full sm:w-64">
              <div className="w-full flex flex-col gap-1.5">
                <label htmlFor="name" className="text-sm font-medium text-(--ink)">Nombre</label>
                <input
                  type="text"
                  id="name"
                  className="field"
                  value={user?.name ?? ""}
                  onChange={(e) => {
                    const value = e.target.value;
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
                  disabled={noEdit}
                />
              </div>
              <div className="w-full flex flex-col gap-1.5">
                <label htmlFor="lastname" className="text-sm font-medium text-(--ink)">Apellido</label>
                <input
                  type="text"
                  id="lastname"
                  className="field"
                  value={user?.lastname ?? ""}
                  onChange={(e) => {
                    const value = e.target.value;
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
                  disabled={noEdit}
                />
              </div>
              <div className="w-full flex flex-col gap-1.5">
                <label htmlFor="new-password" className="text-sm font-medium text-(--ink)">Nueva Contraseña</label>
                <input
                  type="password"
                  id="new-password"
                  className="field"
                  placeholder="Nueva contraseña"
                  onChange={(e) => {
                    const value = e.target.value;
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
                  disabled={noEdit}
                />
              </div>
            </section>
            <section className="flex flex-col flex-nowrap gap-4 w-full sm:w-64">
              <div className="w-full flex flex-col gap-1.5">
                <label htmlFor="rol" className="text-sm font-medium text-(--ink)">Rol</label>
                <input type="text" id="rol" className="field" placeholder={user?.role} disabled />
              </div>
              <div className="w-full flex flex-col gap-1.5">
                <label htmlFor="status" className="text-sm font-medium text-(--ink)">Estatus</label>
                <input type="text" id="status" className="field" placeholder={user?.status} disabled />
              </div>
              <div className="w-full flex flex-col gap-1.5">
                <label htmlFor="confirm-password" className="text-sm font-medium text-(--ink)">Confirmar Contraseña</label>
                <input
                  type="password"
                  id="confirm-password"
                  className="field"
                  placeholder="Confirmar contraseña"
                  onChange={(e) => {
                    const value = e.target.value;
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
                  disabled={noEdit}
                />
                <span className={`text-xs text-(--red) ${(!newPassword || validatePassword()) ? 'hidden' : 'visible'}`}>* Contraseñas deben coincidir</span>
              </div>
            </section>
          </div>
        </section>
        <section className="w-full mt-2 flex flex-row justify-center">
          <button
            onClick={() => { handlerSaveUser(); }}
            className="btn btn-primary"
            disabled={save}
          >
            Guardar Configuración
          </button>
        </section>
      </div>
    </main>
  );
}
