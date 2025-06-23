import NavbarAdminComponent from "@/app/components/navbar/admin";
import InterfaceChangesListComponent from "@/app/components/list/changes";
import styles from './history.module.css';
import { interfacesMock } from "@/mocks/interfaces";


export default function HistoryPersonalPage() {
    return (
        <main>
            <NavbarAdminComponent />
            <div className={styles.history}>
                <section id="download" className={styles.sectionDownload}>
                    <div id="description" className="flex flex-col">
                        <h1>Histórico del Día</h1>
                        <p>Descarga todos los datos de las interfaces con cambios detectados en el día.</p>
                    </div>
                    <button className={styles.btn}>Descargar</button>
                </section>
                <section id="review" className={styles.sectionReview}>
                    <div id="description" className="flex flex-col">
                        <h1>Histórico de Asignaciones</h1>
                        <p>Seleccione un usuario para ver sus interfaces asignadas y su estatus de revisión.</p>
                    </div>
                    <div className="h-fit flex flex-row flex-nowrap justify-between items-center">
                        <div className={styles.selectUser}>
                            <label htmlFor="assign">Usuario</label>
                            <select name="assing" id="assing">
                                <option value="user1">user1</option>
                                <option value="user2">user2</option>
                            </select>
                        </div>
                        <button className={styles.btn}>Descargar Historial de Usuario</button>
                    </div>
                </section>
                <InterfaceChangesListComponent title="Interfaces Asignadas" interfaces={interfacesMock} />
            </div>
        </main>
    );
}