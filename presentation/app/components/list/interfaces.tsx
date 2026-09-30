"use client";

import Image from "next/image";
import { useState, useEffect } from "react";
import { InterfaceChangeSchema } from "@/schemas/interface";
import DiffField from "./diffField";

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
          ci.id_old !== interfaceChangeSchemas.id_old ||
          ci.id_new !== interfaceChangeSchemas.id_new
      )
    );
  };

  const handlerSelectAll = () => {
    setSelectedInterfaces(content.interfaces);
  };

  const handlerDeselectAll = () => {
    setSelectedInterfaces([]);
  };

  useEffect(() => {
    content.onChange(selectedInterfaces);
  }, [selectedInterfaces]);

  useEffect(() => {
    setSelectedInterfaces([]);
  }, [content.interfaces]);

  return (
    <div className="card w-full min-w-fit mb-4 overflow-hidden">
      <section className="w-full py-3 px-4 border-b border-(--gray-light) bg-(--white) flex justify-between items-center">
        <h2 className="font-display m-0 text-(--ink) text-base font-semibold">
          {content.title}
        </h2>
        <button
          className={`btn ${selectedInterfaces.length > 0 ? 'btn-danger' : 'btn-success'}`}
          onClick={() => {
            if (selectedInterfaces.length > 0) handlerDeselectAll();
            else handlerSelectAll();
          }}
          disabled={content.interfaces.length <= 0}
        >
          {selectedInterfaces.length > 0 ? "Deseleccionar Todos" : "Seleccionar Todos"}
        </button>
      </section>
      <section className="w-full flex flex-col divide-y divide-(--gray-light)">
        {content.interfaces.length > 0 &&
          content.interfaces.map(
            (interfaceChangeSchemas: InterfaceChangeSchema, index: number) => {
              return (
                <div key={index} className="w-full flex flex-col gap-3 py-4 px-4">
                  <div className="w-full flex flex-col md:flex-row md:items-center flex-wrap gap-x-6 gap-y-2 justify-between">
                    <div className="flex flex-row flex-wrap items-center gap-x-6 gap-y-2">
                      <Image
                        src="/interfaces/icon.svg"
                        alt="interface"
                        width={20}
                        height={20}
                      />
                      <span className="text-sm text-(--gray)">
                        Asignado a{" "}
                        <span className="font-medium text-(--ink)">
                          {interfaceChangeSchemas.username ?? "No Asignado"}
                        </span>
                      </span>
                      <span className="font-mono text-sm text-(--ink)">
                        {interfaceChangeSchemas.ip_new}
                      </span>
                      <span className="font-mono text-sm text-(--gray)">
                        {interfaceChangeSchemas.community_new}
                      </span>
                      <span className="font-mono text-sm text-(--gray)">
                        {interfaceChangeSchemas.sysname_new}
                      </span>
                      <span className="font-mono text-sm text-(--gray)">
                        ifIndex {interfaceChangeSchemas.ifIndex_new}
                      </span>
                    </div>
                    <input
                      type="checkbox"
                      className="checkbox"
                      checked={selectedInterfaces.includes(interfaceChangeSchemas)}
                      onChange={() =>
                        selectedInterfaces.includes(interfaceChangeSchemas)
                          ? removeInterface(interfaceChangeSchemas)
                          : addInterface(interfaceChangeSchemas)
                      }
                    />
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-x-6 gap-y-3 rounded-[var(--radius)] bg-(--surface) p-3">
                    <DiffField label="ifName" oldValue={interfaceChangeSchemas.ifName_old} newValue={interfaceChangeSchemas.ifName_new} />
                    <DiffField label="ifDescr" oldValue={interfaceChangeSchemas.ifDescr_old} newValue={interfaceChangeSchemas.ifDescr_new} />
                    <DiffField label="ifAlias" oldValue={interfaceChangeSchemas.ifAlias_old} newValue={interfaceChangeSchemas.ifAlias_new} />
                    <DiffField label="ifHighSpeed" oldValue={interfaceChangeSchemas.ifHighSpeed_old} newValue={interfaceChangeSchemas.ifHighSpeed_new} />
                    <DiffField label="ifOperStatus" oldValue={interfaceChangeSchemas.ifOperStatus_old} newValue={interfaceChangeSchemas.ifOperStatus_new} />
                    <DiffField label="ifAdminStatus" oldValue={interfaceChangeSchemas.ifAdminStatus_old} newValue={interfaceChangeSchemas.ifAdminStatus_new} />
                  </div>
                </div>
              );
            }
          )}
        {content.interfaces.length <= 0 && (
          <div className="w-full flex flex-row justify-center items-center py-8">
            <p className="text-(--gray) text-sm">No hay interfaces.</p>
          </div>
        )}
      </section>
    </div>
  );
}
