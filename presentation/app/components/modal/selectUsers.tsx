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
    <div id="modal-state" className="absolute z-40" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <aside className="fixed inset-0 bg-(--ink)/50 backdrop-blur-[2px] transition-opacity" aria-hidden="true"></aside>
      <div className="fixed inset-0 z-40 w-screen overflow-y-auto">
        <div id="modal-panel" className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <div className="relative transform overflow-hidden rounded-xl bg-(--white) text-left shadow-[var(--shadow-modal)] transition-all sm:my-8 sm:w-full sm:max-w-lg">
            <section className="px-6 pt-6 pb-4">
              <h3 className="font-display m-0 text-lg font-semibold text-(--ink)" id="modal-title">Selección de Usuarios</h3>
              <p className="text-sm text-(--gray) pb-4 mt-1">Seleccione los usuarios que desea asignar las interfaces con cambios.</p>
              <div className="w-full grid grid-cols-3 gap-3">
                {props.users.map((user: UserSchema, index: number) => {
                  return (
                    <div key={index} className='flex flex-row gap-2 items-center'>
                      <input
                        type="checkbox"
                        className="checkbox"
                        onClick={() => {
                          if (selectedUsers.includes(user)) removeUser(user);
                          else addUser(user);
                        }}
                      />
                      <p className="text-sm text-(--ink)">{user.name} {user.lastname}</p>
                    </div>
                  )
                })}
              </div>
            </section>
            <section className="px-6 pb-6 flex justify-end gap-3">
              <button
                id="modal-cancel"
                type="button"
                className="btn btn-secondary"
                onClick={() => {
                  if (props.onCancel) props.onCancel();
                }}
              >
                Cancelar
              </button>
              <button
                id="modal-accept"
                type="button"
                className="btn btn-primary"
                onClick={() => {
                  if (props.onAccept) props.onAccept(selectedUsers);
                }}
              >
                Aceptar
              </button>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
}
