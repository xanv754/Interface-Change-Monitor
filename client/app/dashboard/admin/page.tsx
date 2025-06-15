import NavbarAdminComponent from "../../components/navbar/admin";
import CardComponent from "../../components/card/main";
import { StatusOption } from "../../components/card/main";
import InterfacesListComponent from "../../components/list/interfaces";
import styles from './dashboard.module.css';
import { interfacesMock } from "@/mocks/interfaces";


export default function DashboardPage() {
    return (
        <main>
            <NavbarAdminComponent />
            <section className={styles.cardStatistics}>
                <CardComponent title="Interfaces con Cambios Detectados Hoy" total={12} status={StatusOption.NORMAL} />
                <CardComponent title="Interfaces Pendientes por Revisión" total={5} status={StatusOption.PENDING} />
                <CardComponent title="Interfaces Revisadas" total={5} status={StatusOption.REVIEW} />
            </section>
            <section className={styles.assignment}>
                <h3>Asignación de Interfaces</h3>
                <p>Seleccione interfaces con cambios para asignar a un usuario o asigne automáticamente todas las interfaces con cambios a los usuarios disponibles.</p>
                <div className={styles.buttonsAssignment}>
                    <button className={styles.btn} disabled>Asignación Automática</button>
                    <div className={styles.confirmAssignment}>
                        <div className={styles.selectorAssign}>
                            <label htmlFor="assign">Asignar a</label>
                            <select name="assing" id="assing" disabled>
                                <option value="user1">user1</option>
                                <option value="user2">user2</option>
                            </select>
                        </div>
                        <button className={styles.btn} disabled>Asignar</button>
                    </div>
                </div>
            </section>
            <section className={styles.listInterfaces}>
                <InterfacesListComponent title="Interfaces con Cambios" interfaces={interfacesMock} />
            </section>
        </main>
    );
}