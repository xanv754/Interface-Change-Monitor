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
                <CardComponent title="Interfaces Revisadas" total={5} status={StatusOption.REVIEW} />
            </section>
            <section className={`${styles.assignment} w-full p-4 flex flex-col justify-between`}>
                <h3>Interfaces Asignadas</h3>
                <p>Seleccione interfaces para cambiar su estatus.</p>
                <div className="h-14 flex flex-row flex-wrap justify-between p-0 pt-4">
                    <div className={styles.box}>
                        <label htmlFor="assign">Buscar</label>
                        <input type="text" className={styles.inputFilter} placeholder="Dato de la interfaz"/>
                    </div>
                    <div className={styles.box}>
                        <label htmlFor="assign">Estatus</label>
                        <select name="assing" id="assing">
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