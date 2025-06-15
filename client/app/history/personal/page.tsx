import NavbarStandardComponent from "@/app/components/navbar/standard";
import InterfacesListComponent from "@/app/components/list/interfaces";
import CardComponent from "@/app/components/card/main";
import styles from './history.module.css';
import { StatusOption } from "@/app/components/card/main";
import { interfacesMock } from "@/mocks/interfaces";


export default function HistoryPersonalPage() {
    return (
        <main>
            <NavbarStandardComponent />
            <div className={styles.history}>
                <section id="review" className={styles.sectionReview}>
                    <div id="description" className="flex flex-col">
                        <h1>Histórico de Asignaciones</h1>
                        <p>Descargue su historial de todas las interfaces asignadas que ya ha revisado.</p>
                    </div>
                    <button className={styles.btn}>Descargar Historial</button>
                </section>
                <section id="statistics" className={styles.sectionStatistics}>
                    <CardComponent title="Interfaces Asignadas" total={12} status={StatusOption.NORMAL} />
                    <CardComponent title="Interfaces Pendientes" total={12} status={StatusOption.PENDING} />
                    <CardComponent title="Interfaces Revisadas" total={12} status={StatusOption.REVIEW} />
                </section>
                <section id="description" className={styles.sectionAssignments}>
                    <h3>Revisión de Histórico</h3>
                    <p>Seleccione interfaces para actualizar su estatus de revisión.</p>
                </section>
                <div className={styles.buttonsAssignment}>
                    <div className={styles.selectorAssign}>
                        <label htmlFor="assign">Estatus</label>
                        <select name="assing" id="assing" disabled>
                            <option value="user1">Pendiente</option>
                            <option value="user1">Revisada</option>
                            <option value="user2">Redescubierta</option>
                        </select>
                    </div>
                    <button className={styles.btn} disabled>Cambiar Estatus</button>
                </div>
                <InterfacesListComponent title="Interfaces Revisadas" interfaces={interfacesMock} />
            </div>
        </main>
    );
}