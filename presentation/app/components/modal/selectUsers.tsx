"use client";

import React, { useState } from 'react';
import { UserSchema } from '@/schemas/user';

interface ModalProps {
  users: UserSchema[];
  onAccept: (users: UserSchema[]) => void;
  onCancel: () => void;
}

export default function SelectUsersModalComponent(props: ModalProps) {
  const [selectedUsers, setSelectedUsers] = useState<UserSchema[]>([]);

  const addUser = (user: UserSchema) => {
    setSelectedUsers([...selectedUsers, user]);
  };

  const removeUser = (user: UserSchema) => {
    setSelectedUsers(selectedUsers.filter((selectedUser) => selectedUser.username !== user.username));
  };

  return (
    <div id="modal-state" className="absolute z-10" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <aside className="fixed inset-0 bg-black/55 transition-opacity" aria-hidden="true"></aside>
      <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
        <div id="modal-panel" className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <div className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
            <section className="bg-gray-50 px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
              <div className="sm:flex sm:items-start">
                <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                  <h3 className="text-base font-semibold leading-6 text-gray-600" id="modal-title">Selección de Usuarios</h3>
                  <p className="text-md text-gray-500 pb-3">Seleccione los usuarios que desea asignar las interfaces con cambios.</p>
                  <div className="w-full grid grid-cols-3 gap-4">
                    {props.users.map((user: UserSchema, index: number) => {
                      return (
                        <div key={index} className='flex flex-row gap-2 items-center'>
                          <input
                            type="checkbox"
                            className="w-5 h-5 cursor-pointer"
                            onClick={() => {
                              selectedUsers.includes(user)
                              ? removeUser(user)
                              : addUser(user)
                            }}
                          />
                          <p className="text-sm text-(--blue)">{user.name} {user.lastname}</p>
                        </div>
                      )
                    })}
                  </div>
                </div>
              </div>
            </section>
            <section className="bg-gray-50 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
              <button
                id="modal-accept"
                type="button"
                className="inline-flex w-full justify-center rounded-md bg-(--blue) px-3 py-2 text-sm font-semibold text-white shadow-sm transition-all ease-linear duration-200 hover:bg-blue-700 sm:ml-3 sm:w-auto cursor-pointer"
                onClick={() => {
                  if (props.onAccept) props.onAccept(selectedUsers);
                }}
              >
                Aceptar
              </button>
              <button
                id="modal-cancel"
                type="button"
                className="inline-flex w-full justify-center rounded-md bg-(--red) px-3 py-2 text-sm font-semibold text-white shadow-sm transition-all ease-linear duration-200 hover:bg-blue-700 sm:ml-3 sm:w-auto cursor-pointer"
                onClick={() => {
                  if (props.onCancel) props.onCancel();
                }}
              >
                Cancelar
              </button>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
}