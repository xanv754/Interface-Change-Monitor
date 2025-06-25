import NavbarAdminComponent from "../components/navbar/admin";
import Image from "next/image";
import styles from './settings.module.css';


export default function SettingsPage() {
    return (
        <main>
            <NavbarAdminComponent />
            <div className="w-full p-4 flex flex-col flex-nowrap gap-4">
                <section className="w-full flex flex-row justify-end">
                    <button className="w-fit h-fit">
                        <Image
                            src="/buttons/edit.svg"
                            alt="edit"
                            width={24}
                            height={24}
                        />
                    </button>
                </section>
                <section className={styles.sectionSetting}>
                    <h1 className="pb-4">Notificaciones de Cambios</h1>
                    <div id="notifications" className="flex flex-row flex-nowrap items-center gap-10">
                        <div className={`${styles.notificationOptions} w-fit flex flex-col gap-4`}>
                            <h3 id="notification-option">Notificar Cambios en el Campo "ifName"</h3>
                            <h3 id="notification-option">Notificar Cambios en el Campo "ifDescr"</h3>
                            <h3 id="notification-option">Notificar Cambios en el Campo "ifAlias"</h3>
                        </div>
                        <div className={`w-fit flex flex-col gap-4`}>
                            <label className={`${styles.switch}`}>
                                <input type="checkbox" />
                                <span className={`${styles.slider}`}></span>
                            </label>
                            <label className={`${styles.switch}`}>
                                <input type="checkbox" />
                                <span className={`${styles.slider}`}></span>
                            </label>
                            <label className={`${styles.switch}`}>
                                <input type="checkbox" />
                                <span className={`${styles.slider}`}></span>
                            </label>
                        </div>
                        <div className={`${styles.notificationOptions} w-fit flex flex-col gap-4`}>
                            <h3 id="notification-option">Notificar Cambios en el Campo "ifHighSpeed"</h3>
                            <h3 id="notification-option">Notificar Cambios en el Campo "ifOperStatus"</h3>
                            <h3 id="notification-option">Notificar Cambios en el Campo "ifAdminStatus"</h3>
                        </div>
                        <div className={`w-fit flex flex-col gap-4`}>
                            <label className={`${styles.switch}`}>
                                <input type="checkbox" />
                                <span className={`${styles.slider}`}></span>
                            </label>
                            <label className={`${styles.switch}`}>
                                <input type="checkbox" />
                                <span className={`${styles.slider}`}></span>
                            </label>
                            <label className={`${styles.switch}`}>
                                <input type="checkbox" />
                                <span className={`${styles.slider}`}></span>
                            </label>
                        </div>
                    </div>
                </section>
                <section className={styles.sectionSetting}>
                    <h1 className="pb-4">Permisos de Administradores</h1>
                    <div id="notifications" className="flex flex-row flex-nowrap items-center gap-10">
                        <div className={`${styles.notificationOptions} w-fit flex flex-col gap-4`}>
                            <h3 id="notification-option">Los administradores pueden asignar interfaces</h3>
                            <h3 id="notification-option">Los administradores pueden recibir asignaciones de interfaces</h3>
                            <h3 id="notification-option">Los administradores pueden revisar todas las estadísticas</h3>
                            <h3 id="notification-option">Los administradores pueden cambiar las configuraciones del sistema</h3>
                        </div>
                        <div className={`w-fit flex flex-col gap-4`}>
                            <label className={`${styles.switch}`}>
                                <input type="checkbox" />
                                <span className={`${styles.slider}`}></span>
                            </label>
                            <label className={`${styles.switch}`}>
                                <input type="checkbox" />
                                <span className={`${styles.slider}`}></span>
                            </label>
                            <label className={`${styles.switch}`}>
                                <input type="checkbox" />
                                <span className={`${styles.slider}`}></span>
                            </label>
                            <label className={`${styles.switch}`}>
                                <input type="checkbox" />
                                <span className={`${styles.slider}`}></span>
                            </label>
                        </div>
                    </div>
                </section>
                <section className="w-full flex flex-row justify-center">
                    <button className={styles.btn} disabled>Guardar Configuración</button>
                </section>
            </div>
        </main>
    );
}
