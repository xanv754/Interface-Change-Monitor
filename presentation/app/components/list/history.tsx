"use client";

import Image from "next/image";
import { useState, useEffect } from "react";
import { InterfaceAssignedSchema } from "@/schemas/interface";
import { AssignmentStatusTypes } from "@/constants/types";

/**
 * Component to show a list of interfaces with a title and a list of selected interfaces.
 *
 * @param title - Title of the list.
 * @param interfaces - List of interfaces.
 * @param onChange - Function to handle the selection of interfaces.
 */
interface ListProps {
  title: string;
  interfaces: InterfaceAssignedSchema[];
  onChange: (selectedInterfaces: InterfaceAssignedSchema[]) => void;
}

export default function HistoryInterfaceListComponent(content: ListProps) {
  const [selectedInterfaces, setSelectedInterfaces] = useState<
    InterfaceAssignedSchema[]
  >([]);

  const addInterface = (interfaceChangeSchemas: InterfaceAssignedSchema) => {
    setSelectedInterfaces([...selectedInterfaces, interfaceChangeSchemas]);
  };

  const removeInterface = (interfaceChangeSchemas: InterfaceAssignedSchema) => {
    setSelectedInterfaces(
      selectedInterfaces.filter(
        (ci) =>
          ci.id_old !== interfaceChangeSchemas.id_old &&
          ci.id_new !== interfaceChangeSchemas.id_new
      )
    );
  };

  useEffect(() => {
    content.onChange(selectedInterfaces);
  }, [selectedInterfaces]);

  return (
    <div className="w-full min-w-fit bg-(--white) mb-4 pb-4 flex flex-col gap-4 border-2 border-solid border-(--gray-light) rounded-lg shadow-[0.2em_0.3em_0.5em_rgba(0,0,0,0.2)]">
      <section
        id="header"
        className="w-full py-2 px-0 rounded-tl-lg rounded-tr-lg bg-(--blue) flex justify-center"
      >
        <h2 className="m-0 text-(--white) text-xl font-bold">
          {content.title}
        </h2>
      </section>
      <section id="content" className="w-full flex flex-col gap-8">
        {content.interfaces.length > 0 &&
          content.interfaces.map(
            (interfaceChangeSchemas: InterfaceAssignedSchema, index: number) => {
              return (
                <div
                  key={index}
                  className="w-full flex flex-col gap-2 text-(--gray)"
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
                      <div
                        id="status"
                        className="w-fit flex flex-row gap-2 items-center m-0 font-semibold text-(--blue)"
                      >
                        <h4>Estatus:</h4>
                        <p className="text-(--gray) font-normal">
                          {interfaceChangeSchemas.type_status == AssignmentStatusTypes.PENDING && "Pendiente"}
                          {interfaceChangeSchemas.type_status == AssignmentStatusTypes.INSPECTED && "Revisado"}
                          {interfaceChangeSchemas.type_status == AssignmentStatusTypes.REDISCOVERED && "Revisado (Interfaz Redescubierta)"}
                        </p>
                      </div>
                    </div>
                    <input
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
                    className="w-full flex flex-row flex-nowrap"
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
