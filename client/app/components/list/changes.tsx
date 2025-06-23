"use client";

import Image from "next/image";
import styles from './interfaces.module.css';
import { useState, useEffect, use } from "react";
import { ChangeInterface } from "@/models/changes";

interface ListProps {
    title: string;
    interfaces: ChangeInterface[];
    onChange: (selectedInterfaces: ChangeInterface[]) => void;
}

export default function InterfaceChangesListComponent(content: ListProps) {
    const [selectedInterfaces, setSelectedInterfaces] = useState<ChangeInterface[]>([]);

    const addInterface = (interfaceChange: ChangeInterface) => {
        setSelectedInterfaces([...selectedInterfaces, interfaceChange]);
    }

    const removeInterface = (interfaceChange: ChangeInterface) => {
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
                {content.interfaces.length > 0 && content.interfaces.map((interfaceChange: ChangeInterface, index: number) => {
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
                                        {interfaceChange.username ? <p>{interfaceChange.username}</p> : <p>No Asignado</p> }
                                    </div>
                                    <div id="ip" className={styles.contentBox}>
                                        <h4>IP:</h4>
                                        <p>{interfaceChange.ip_new}</p>
                                    </div>
                                    <div id="community" className={styles.contentBox}>
                                        <h4>Community:</h4>
                                        <p>{interfaceChange.community_new}</p>
                                    </div>
                                    <div id="sysname" className={styles.contentBox}>
                                        <h4>Sysname:</h4>
                                        <p>{interfaceChange.sysname_new}</p>
                                    </div>
                                    <div id="ifIndex" className={styles.contentBox}>
                                        <h4>ifIndex:</h4>
                                        <p>{interfaceChange.ifIndex_new}</p>
                                    </div>
                                </div>
                                <input 
                                    type="checkbox" 
                                    className={styles.selectInterface} 
                                    onChange={() => selectedInterfaces.includes(interfaceChange) ? removeInterface(interfaceChange) : addInterface(interfaceChange)}/>
                            </section>
                            <section id="data" className={styles.contentData}>
                                <div id="old" className={styles.data}>
                                    <h3>Datos Antiguos</h3>
                                    <div id="ifNameOld" className={styles.contentBox}>
                                        <h4 className={interfaceChange.ifName_old !== interfaceChange.ifName_new ? styles.contentBoxChange : ''}>ifName:</h4>
                                        <p>{interfaceChange.ifName_old}</p>
                                    </div>
                                    <div id="ifDescrOld" className={styles.contentBox}>
                                        <h4 className={interfaceChange.ifDescr_old !== interfaceChange.ifDescr_new ? styles.contentBoxChange : ''}>ifDescr:</h4>
                                        <p>{interfaceChange.ifDescr_old}</p>
                                    </div>
                                    <div id="ifAliasOld" className={styles.contentBox}>
                                        <h4 className={interfaceChange.ifAlias_old !== interfaceChange.ifAlias_new ? styles.contentBoxChange : ''}>ifAlias:</h4>
                                        <p>{interfaceChange.ifAlias_old}</p>
                                    </div>
                                    <div id="ifHighSpeedOld" className={styles.contentBox}>
                                        <h4 className={interfaceChange.ifHighSpeed_old !== interfaceChange.ifHighSpeed_new ? styles.contentBoxChange : ''}>ifHighSpeed:</h4>
                                        <p>{interfaceChange.ifHighSpeed_old}</p>
                                    </div>
                                    <div id="ifOperStatusOld" className={styles.contentBox}>
                                        <h4 className={interfaceChange.ifOperStatus_old !== interfaceChange.ifOperStatus_new ? styles.contentBoxChange : ''}>ifOperStatus:</h4>
                                        <p>{interfaceChange.ifOperStatus_old}</p>
                                    </div>
                                    <div id="ifAdminStatusOld" className={styles.contentBox}>
                                        <h4 className={interfaceChange.ifAdminStatus_old !== interfaceChange.ifAdminStatus_new ? styles.contentBoxChange : ''}>ifAdminStatus:</h4>
                                        <p>{interfaceChange.ifAdminStatus_old}</p>
                                    </div>
                                </div>
                                <div id="new" className={styles.data}>
                                    <h3>Datos Actuales</h3>
                                    <div id="ifNameNew" className={styles.contentBox}>
                                        <h4 className={interfaceChange.ifName_old !== interfaceChange.ifName_new ? styles.contentBoxChange : ''}>ifName:</h4>
                                        <p>{interfaceChange.ifName_new}</p>
                                    </div>
                                    <div id="ifDescrNew" className={styles.contentBox}>
                                        <h4 className={interfaceChange.ifDescr_old !== interfaceChange.ifDescr_new ? styles.contentBoxChange : ''}>ifDescr:</h4>
                                        <p>{interfaceChange.ifDescr_new}</p>
                                    </div>
                                    <div id="ifAliasNew" className={styles.contentBox}>
                                        <h4 className={interfaceChange.ifAlias_old !== interfaceChange.ifAlias_new ? styles.contentBoxChange : ''}>ifAlias:</h4>
                                        <p>{interfaceChange.ifAlias_new}</p>
                                    </div>
                                    <div id="ifHighSpeedNew" className={styles.contentBox}>
                                        <h4 className={interfaceChange.ifHighSpeed_old !== interfaceChange.ifHighSpeed_new ? styles.contentBoxChange : ''}>ifHighSpeed:</h4>
                                        <p>{interfaceChange.ifHighSpeed_new}</p>
                                    </div>
                                    <div id="ifOperStatusNew" className={styles.contentBox}>
                                        <h4 className={interfaceChange.ifOperStatus_old !== interfaceChange.ifOperStatus_new ? styles.contentBoxChange : ''}>ifOperStatus:</h4>
                                        <p>{interfaceChange.ifOperStatus_new}</p>
                                    </div>
                                    <div id="ifAdminStatusNew" className={styles.contentBox}>
                                        <h4 className={interfaceChange.ifAdminStatus_old !== interfaceChange.ifAdminStatus_new ? styles.contentBoxChange : ''}>ifAdminStatus:</h4>
                                        <p>{interfaceChange.ifAdminStatus_new}</p>
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