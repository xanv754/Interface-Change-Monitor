"use client";

import Image from "next/image";
import styles from './interfaces.module.css';
import { useState, useEffect } from "react";
import { AssignmentModel } from "@/models/assignments";

interface ListProps {
    title: string;
    interfaces: AssignmentModel[];
    onChange: (selectedInterfaces: AssignmentModel[]) => void;
}

export default function InterfaceAssignmentListComponent(content: ListProps) {
    const [selectedInterfaces, setSelectedInterfaces] = useState<AssignmentModel[]>([]);

    const addInterface = (interfaceChange: AssignmentModel) => {
        setSelectedInterfaces([...selectedInterfaces, interfaceChange]);
    }

    const removeInterface = (interfaceChange: AssignmentModel) => {
        setSelectedInterfaces(selectedInterfaces.filter(ci => ci.id_old !== interfaceChange.id_old && ci.id_new !== interfaceChange.id_new));
    }

    useEffect(() => {
        content.onChange(selectedInterfaces);
    }, [selectedInterfaces]);

    return (
        <div className={styles.table}>
            <section id='header' className={styles.tableHeader}>
                <h2>{content.title}</h2>
            </section>
            <section id='content' className={styles.tableContent}>
                {content.interfaces.length > 0 && content.interfaces.map((assignment: AssignmentModel, index: number) => {
                    return (
                        <div key={index} className={styles.content}>
                            <section className={styles.contentHeader}>
                                <div id="interface" className={styles.contentInterface}>
                                    <Image
                                        src="/interfaces/icon.svg"
                                        alt="interface"
                                        width={24}
                                        height={24}
                                    />
                                    <div id="assigned" className={styles.contentBox}>
                                        <h4>Asignado a:</h4>
                                        {assignment.username ? <p>{assignment.username}</p> : <p>No Asignado</p> }
                                    </div>
                                    <div id="ip" className={styles.contentBox}>
                                        <h4>IP:</h4>
                                        <p>{assignment.ip_new}</p>
                                    </div>
                                    <div id="community" className={styles.contentBox}>
                                        <h4>Community:</h4>
                                        <p>{assignment.community_new}</p>
                                    </div>
                                    <div id="sysname" className={styles.contentBox}>
                                        <h4>Sysname:</h4>
                                        <p>{assignment.sysname_new}</p>
                                    </div>
                                    <div id="ifIndex" className={styles.contentBox}>
                                        <h4>ifIndex:</h4>
                                        <p>{assignment.ifIndex_new}</p>
                                    </div>
                                </div>
                                <input 
                                    type="checkbox" 
                                    className={styles.selectInterface} 
                                    onChange={() => selectedInterfaces.includes(assignment) ? removeInterface(assignment) : addInterface(assignment)}/>
                            </section>
                            <section id="data" className={styles.contentData}>
                                <div id="old" className={styles.data}>
                                    <h3>Datos Antiguos</h3>
                                    <div id="ifNameOld" className={styles.contentBox}>
                                        <h4 className={assignment.ifName_old !== assignment.ifName_new ? styles.contentBoxChange : ''}>ifName:</h4>
                                        <p>{assignment.ifName_old}</p>
                                    </div>
                                    <div id="ifDescrOld" className={styles.contentBox}>
                                        <h4 className={assignment.ifDescr_old !== assignment.ifDescr_new ? styles.contentBoxChange : ''}>ifDescr:</h4>
                                        <p>{assignment.ifDescr_old}</p>
                                    </div>
                                    <div id="ifAliasOld" className={styles.contentBox}>
                                        <h4 className={assignment.ifAlias_old !== assignment.ifAlias_new ? styles.contentBoxChange : ''}>ifAlias:</h4>
                                        <p>{assignment.ifAlias_old}</p>
                                    </div>
                                    <div id="ifHighSpeedOld" className={styles.contentBox}>
                                        <h4 className={assignment.ifHighSpeed_old !== assignment.ifHighSpeed_new ? styles.contentBoxChange : ''}>ifHighSpeed:</h4>
                                        <p>{assignment.ifHighSpeed_old}</p>
                                    </div>
                                    <div id="ifOperStatusOld" className={styles.contentBox}>
                                        <h4 className={assignment.ifOperStatus_old !== assignment.ifOperStatus_new ? styles.contentBoxChange : ''}>ifOperStatus:</h4>
                                        <p>{assignment.ifOperStatus_old}</p>
                                    </div>
                                    <div id="ifAdminStatusOld" className={styles.contentBox}>
                                        <h4 className={assignment.ifAdminStatus_old !== assignment.ifAdminStatus_new ? styles.contentBoxChange : ''}>ifAdminStatus:</h4>
                                        <p>{assignment.ifAdminStatus_old}</p>
                                    </div>
                                </div>
                                <div id="new" className={styles.data}>
                                    <h3>Datos Actuales</h3>
                                    <div id="ifNameNew" className={styles.contentBox}>
                                        <h4 className={assignment.ifName_old !== assignment.ifName_new ? styles.contentBoxChange : ''}>ifName:</h4>
                                        <p>{assignment.ifName_new}</p>
                                    </div>
                                    <div id="ifDescrNew" className={styles.contentBox}>
                                        <h4 className={assignment.ifDescr_old !== assignment.ifDescr_new ? styles.contentBoxChange : ''}>ifDescr:</h4>
                                        <p>{assignment.ifDescr_new}</p>
                                    </div>
                                    <div id="ifAliasNew" className={styles.contentBox}>
                                        <h4 className={assignment.ifAlias_old !== assignment.ifAlias_new ? styles.contentBoxChange : ''}>ifAlias:</h4>
                                        <p>{assignment.ifAlias_new}</p>
                                    </div>
                                    <div id="ifHighSpeedNew" className={styles.contentBox}>
                                        <h4 className={assignment.ifHighSpeed_old !== assignment.ifHighSpeed_new ? styles.contentBoxChange : ''}>ifHighSpeed:</h4>
                                        <p>{assignment.ifHighSpeed_new}</p>
                                    </div>
                                    <div id="ifOperStatusNew" className={styles.contentBox}>
                                        <h4 className={assignment.ifOperStatus_old !== assignment.ifOperStatus_new ? styles.contentBoxChange : ''}>ifOperStatus:</h4>
                                        <p>{assignment.ifOperStatus_new}</p>
                                    </div>
                                    <div id="ifAdminStatusNew" className={styles.contentBox}>
                                        <h4 className={assignment.ifAdminStatus_old !== assignment.ifAdminStatus_new ? styles.contentBoxChange : ''}>ifAdminStatus:</h4>
                                        <p>{assignment.ifAdminStatus_new}</p>
                                    </div>
                                </div>
                            </section>
                        </div>
                    );
                })}
                {content.interfaces.length <= 0 && 
                    <div className="w-full flex flex-row justify-center items-center">
                        <p className="text-gray-400">No hay interfaces asignadas.</p>
                    </div>
                }
            </section>
        </div>
    );
}