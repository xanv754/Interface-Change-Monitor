"use client";

import Image from "next/image";
import { useState, useEffect } from "react";
import { InterfaceChangeSchema } from "@/schemas/interface";

/**
 * Component to show a list of interfaces with a title and a list of selected interfaces.
 *
 * @param title - Title of the list.
 * @param interfaces - List of interfaces.
 * @param onChange - Function to handle the selection of interfaces.
 */
interface ListProps {
  title: string;
  interfaces: InterfaceChangeSchema[];
  onChange: (selectedInterfaces: InterfaceChangeSchema[]) => void;
}

export default function InterfaceListComponent(content: ListProps) {
  const [selectedInterfaces, setSelectedInterfaces] = useState<
    InterfaceChangeSchema[]
  >([]);

  const addInterface = (interfaceChangeSchemas: InterfaceChangeSchema) => {
    setSelectedInterfaces([...selectedInterfaces, interfaceChangeSchemas]);
  };

  const removeInterface = (interfaceChangeSchemas: InterfaceChangeSchema) => {
    setSelectedInterfaces(
      selectedInterfaces.filter(
        (ci) =>
          ci.id_old !== interfaceChangeSchemas.id_old &&
          ci.id_new !== interfaceChangeSchemas.id_new
      )
    );
  };

  const handlerSelectAll = () => {
    setSelectedInterfaces(content.interfaces);
    const checkboxes = document.querySelectorAll("#checkbox-select") as NodeListOf<HTMLInputElement>;
    checkboxes.forEach((checkbox) => {
      checkbox.checked = true;
    });
  };

  const handlerDeselectAll = () => {
    setSelectedInterfaces([]);
    const checkboxes = document.querySelectorAll("#checkbox-select") as NodeListOf<HTMLInputElement>;
    checkboxes.forEach((checkbox) => {
      checkbox.checked = false;
    });
  };

  useEffect(() => {
    content.onChange(selectedInterfaces);
  }, [selectedInterfaces]);

  return (
    <div className="w-full min-w-fit bg-(--white) mb-4 pb-4 flex flex-col gap-4 border-2 border-solid border-(--gray-light) rounded-lg shadow-[0.2em_0.3em_0.5em_rgba(0,0,0,0.2)]">
      <section
        id="header"
        className="w-full py-2 px-4 rounded-tl-lg rounded-tr-lg bg-(--blue) flex justify-between"
      >
        <h2 className="m-0 text-(--white) text-xl font-bold">
          {content.title}
        </h2>
        <button 
          className={`w-fit h-full ${selectedInterfaces.length > 0 ? 'bg-(--red)' : 'bg-(--green)'} px-4 rounded-md text-(--white) transition-all duration-300 ease-in-out cursor-pointer active:bg-(--red-bright) hover:bg-(--red-dark) disabled:bg-(--gray) disabled:text-(--gray-light) disabled:cursor-not-allowed`}
          onClick={() => { 
            if (selectedInterfaces.length > 0) handlerDeselectAll();
            else handlerSelectAll();
          }}
          disabled={content.interfaces.length <= 0}
        >
          {selectedInterfaces.length > 0 ? "Deseleccionar Todos" : "Seleccionar Todos"}
        </button>
      </section>
      <section id="content" className="w-full flex flex-col gap-8">
        {content.interfaces.length > 0 &&
          content.interfaces.map(
            (interfaceChangeSchemas: InterfaceChangeSchema, index: number) => {
              return (
                <div
                  key={index}
                  className="w-full flex flex-col gap-2 text-(--gray) border-b-2 border-solid border-(--gray-light)"
                >
                  <section className="w-full flex flex-col md:flex-row flex-nowrap justify-between py-0 px-3.5">
                    <div
                      id="interface"
                      className="w-fit flex flex-row flex-nowrap gap-6"
                    >
                      <Image
                        src="/interfaces/icon.svg"
                        alt="interface"
                        width={24}
                        height={24}
                      />
                      <div
                        id="assigned"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4>Asignado a:</h4>
                        {interfaceChangeSchemas.username ? (
                          <p className="text-(--gray) font-normal">
                            {interfaceChangeSchemas.username}
                          </p>
                        ) : (
                          <p className="text-(--gray) font-normal">
                            No Asignado
                          </p>
                        )}
                      </div>
                      <div
                        id="ip"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4>IP:</h4>
                        <p className="text-(--gray) font-normal">
                          {interfaceChangeSchemas.ip_new}
                        </p>
                      </div>
                      <div
                        id="community"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4>Community:</h4>
                        <p className="text-(--gray) font-normal">
                          {interfaceChangeSchemas.community_new}
                        </p>
                      </div>
                      <div
                        id="sysname"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4>Sysname:</h4>
                        <p className="text-(--gray) font-normal">
                          {interfaceChangeSchemas.sysname_new}
                        </p>
                      </div>
                      <div
                        id="ifIndex"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4>ifIndex:</h4>
                        <p className="text-(--gray) font-normal">
                          {interfaceChangeSchemas.ifIndex_new}
                        </p>
                      </div>
                    </div>
                    <input
                      id="checkbox-select"
                      type="checkbox"
                      className="w-5 h-5 cursor-pointer"
                      onChange={() =>
                        selectedInterfaces.includes(interfaceChangeSchemas)
                          ? removeInterface(interfaceChangeSchemas)
                          : addInterface(interfaceChangeSchemas)
                      }
                    />
                  </section>
                  <section
                    id="data"
                    className="w-full flex flex-row flex-nowrap pb-8"
                  >
                    <div id="old" className="w-2/4 flex flex-col py-0 px-8">
                      <h3 className="text-(--gray) font-bold">
                        Datos Antiguos
                      </h3>
                      <div
                        id="ifNameOld"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4
                          className={
                            interfaceChangeSchemas.ifName_old !==
                            interfaceChangeSchemas.ifName_new
                              ? "text-(--red)"
                              : ""
                          }
                        >
                          ifName:
                        </h4>
                        <p className="text-(--gray) font-normal">
                          {interfaceChangeSchemas.ifName_old}
                        </p>
                      </div>
                      <div
                        id="ifDescrOld"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4
                          className={
                            interfaceChangeSchemas.ifDescr_old !==
                            interfaceChangeSchemas.ifDescr_new
                              ? "text-(--red)"
                              : ""
                          }
                        >
                          ifDescr:
                        </h4>
                        <p className="text-(--gray) font-normal">
                          {interfaceChangeSchemas.ifDescr_old}
                        </p>
                      </div>
                      <div
                        id="ifAliasOld"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4
                          className={
                            interfaceChangeSchemas.ifAlias_old !==
                            interfaceChangeSchemas.ifAlias_new
                              ? "text-(--red)"
                              : ""
                          }
                        >
                          ifAlias:
                        </h4>
                        <p className="text-(--gray) font-normal">
                          {interfaceChangeSchemas.ifAlias_old}
                        </p>
                      </div>
                      <div
                        id="ifHighSpeedOld"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4
                          className={
                            interfaceChangeSchemas.ifHighSpeed_old !==
                            interfaceChangeSchemas.ifHighSpeed_new
                              ? "text-(--red)"
                              : ""
                          }
                        >
                          ifHighSpeed:
                        </h4>
                        <p className="text-(--gray) font-normal">
                          {interfaceChangeSchemas.ifHighSpeed_old}
                        </p>
                      </div>
                      <div
                        id="ifOperStatusOld"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4
                          className={
                            interfaceChangeSchemas.ifOperStatus_old !==
                            interfaceChangeSchemas.ifOperStatus_new
                              ? "text-(--red)"
                              : ""
                          }
                        >
                          ifOperStatus:
                        </h4>
                        <p className="text-(--gray) font-normal">
                          {interfaceChangeSchemas.ifOperStatus_old}
                        </p>
                      </div>
                      <div
                        id="ifAdminStatusOld"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4
                          className={
                            interfaceChangeSchemas.ifAdminStatus_old !==
                            interfaceChangeSchemas.ifAdminStatus_new
                              ? "text-(--red)"
                              : ""
                          }
                        >
                          ifAdminStatus:
                        </h4>
                        <p className="text-(--gray) font-normal">
                          {interfaceChangeSchemas.ifAdminStatus_old}
                        </p>
                      </div>
                    </div>
                    <div id="new" className="w-2/4 flex flex-col py-0 px-8">
                      <h3 className="text-(--gray) font-bold">
                        Datos Actuales
                      </h3>
                      <div
                        id="ifNameNew"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4
                          className={
                            interfaceChangeSchemas.ifName_old !==
                            interfaceChangeSchemas.ifName_new
                              ? "text-(--red)"
                              : ""
                          }
                        >
                          ifName:
                        </h4>
                        <p className="text-(--gray) font-normal">
                          {interfaceChangeSchemas.ifName_new}
                        </p>
                      </div>
                      <div
                        id="ifDescrNew"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4
                          className={
                            interfaceChangeSchemas.ifDescr_old !==
                            interfaceChangeSchemas.ifDescr_new
                              ? "text-(--red)"
                              : ""
                          }
                        >
                          ifDescr:
                        </h4>
                        <p className="text-(--gray) font-normal">
                          {interfaceChangeSchemas.ifDescr_new}
                        </p>
                      </div>
                      <div
                        id="ifAliasNew"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4
                          className={
                            interfaceChangeSchemas.ifAlias_old !==
                            interfaceChangeSchemas.ifAlias_new
                              ? "text-(--red)"
                              : ""
                          }
                        >
                          ifAlias:
                        </h4>
                        <p className="text-(--gray) font-normal">
                          {interfaceChangeSchemas.ifAlias_new}
                        </p>
                      </div>
                      <div
                        id="ifHighSpeedNew"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4
                          className={
                            interfaceChangeSchemas.ifHighSpeed_old !==
                            interfaceChangeSchemas.ifHighSpeed_new
                              ? "text-(--red)"
                              : ""
                          }
                        >
                          ifHighSpeed:
                        </h4>
                        <p className="text-(--gray) font-normal">
                          {interfaceChangeSchemas.ifHighSpeed_new}
                        </p>
                      </div>
                      <div
                        id="ifOperStatusNew"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4
                          className={
                            interfaceChangeSchemas.ifOperStatus_old !==
                            interfaceChangeSchemas.ifOperStatus_new
                              ? "text-(--red)"
                              : ""
                          }
                        >
                          ifOperStatus:
                        </h4>
                        <p className="text-(--gray) font-normal">
                          {interfaceChangeSchemas.ifOperStatus_new}
                        </p>
                      </div>
                      <div
                        id="ifAdminStatusNew"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4
                          className={
                            interfaceChangeSchemas.ifAdminStatus_old !==
                            interfaceChangeSchemas.ifAdminStatus_new
                              ? "text-(--red)"
                              : ""
                          }
                        >
                          ifAdminStatus:
                        </h4>
                        <p className="text-(--gray) font-normal">
                          {interfaceChangeSchemas.ifAdminStatus_new}
                        </p>
                      </div>
                    </div>
                  </section>
                </div>
              );
            }
          )}
        {content.interfaces.length <= 0 && (
          <div className="w-full flex flex-row justify-center items-center">
            <p className="text-gray-400">No hay interfaces.</p>
          </div>
        )}
      </section>
    </div>
  );
}
