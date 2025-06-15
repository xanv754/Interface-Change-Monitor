import NavbarStandardComponent from "../../components/navbar/standard";
import CardComponent from "../../components/card/main";
import InterfacesListComponent from "../../components/list/interfaces";
import styles from './dashboard.module.css';
import { StatusOption } from "../../components/card/main";
import { interfacesMock } from "@/mocks/interfaces";


export default function DashboardPage() {
    return (
        <main>
            <NavbarStandardComponent />
            <section className={styles.cardStatistics}>
                <CardComponent title="Interfaces Asignadas Hoy" total={12} status={StatusOption.NORMAL} />
                <CardComponent title="Interfaces Pendientes" total={5} status={StatusOption.PENDING} />
            </section>
            <section className={styles.assignment}>
                <h3>Interfaces Asignadas</h3>
                <p>Seleccione interfaces para cambiar su estatus.</p>
                <div className={styles.buttonsAssignment}>
                    <div className={styles.selectorAssign}>
                        <label htmlFor="assign">Estatus</label>
                        <select name="assing" id="assing" disabled>
                            <option value="user1">Revisada</option>
                            <option value="user2">Redescubierta</option>
                        </select>
                    </div>
                    <button className={styles.btn} disabled>Cambiar Estatus</button>
                </div>
            </section>
            <section className={styles.listInterfaces}>
                <InterfacesListComponent title="Interfaces con Cambios" interfaces={interfacesMock} />
            </section>
        </main>
    );
}