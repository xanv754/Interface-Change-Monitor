import NavbarAdminComponent from "../components/navbar/admin";
import NavbarStandardComponent from "../components/navbar/standard";
import Image from "next/image";
import styles from './profile.module.css';


export default function ProfilePage() {
    return (
        <main>
            <NavbarAdminComponent />
            <div className="w-full p-4 flex flex-col flex-nowrap gap-2">
                <section className="w-full flex flex-row justify-between items-center">
                    <h1 className={styles.title}>Datos de Personales</h1>
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
                    <div className="flex flex-col">
                        <Image
                            src="/user/alternative.svg"
                            alt="user"
                            width={128}
                            height={128}
                        />
                        <h2>unittest</h2>
                    </div>
                    <div className="flex flex-row flex-nowrap gap-10">
                        <section className="flex flex-col flex-nowrap gap-2">
                            <div className="w-fit h-fit flex flex-col justify-center">
                                <label htmlFor="name" className={styles.fieldLabel}>Nombre</label>
                                <input type="text" id="name" className={styles.fieldInput} placeholder="Nombre" />
                            </div>
                            <div className="w-fit h-fit flex flex-col justify-center">
                                <label htmlFor="lastname" className={styles.fieldLabel}>Apellido</label>
                                <input type="text" id="lastname" className={styles.fieldInput} placeholder="Apellido" />
                            </div>
                            <div className="w-fit h-fit flex flex-col justify-center">
                                <label htmlFor="password" className={styles.fieldLabel}>Contraseña</label>
                                <input type="password" id="password" className={styles.fieldInput} placeholder="Nueva Contraseña" />
                            </div>
                        </section>
                        <section className="flex flex-col flex-nowrap gap-2">
                            <div className="w-fit h-fit flex flex-col justify-center">
                                <label htmlFor="rol" className={styles.fieldLabel}>Rol</label>
                                <input type="text" id="rol" className={styles.fieldInput} placeholder="Rol" disabled />
                            </div>
                            <div className="w-fit h-fit flex flex-col justify-center">
                                <label htmlFor="status" className={styles.fieldLabel}>Estatus</label>
                                <input type="text" id="status" className={styles.fieldInput} placeholder="Estatus" disabled />
                            </div>
                            <div className="w-fit h-fit flex flex-col justify-center">
                                <label htmlFor="confirm-password" className={styles.fieldLabel}>Confirmar Contraseña</label>
                                <input type="password" id="confirm-password" className={styles.fieldInput} placeholder="Confirmar Contraseña" />
                            </div>
                        </section>
                    </div>
                </section>
                <section className="w-full mt-4 flex flex-row justify-center">
                    <button className={styles.btn} disabled>Guardar Configuración</button>
                </section>
            </div>
        </main>
    );
}