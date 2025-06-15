import NavbarAdminComponent from "../components/navbar/admin";
import CardComponent from "../components/card/main";
import BarChartComponent from "../components/chart/bar";
import Image from "next/image";
import styles from './statistics.module.css';
import { StatusOption } from "../components/card/main";


export default function StatisticsPage() {
    return (
        <main>
            <NavbarAdminComponent />
            <section id="statistics-general" className="w-full px-4 flex flex-row flex-nowrap gap-4">
                <CardComponent title="Interfaces con Cambios Detectados" total={12} status={StatusOption.NORMAL} />
                <CardComponent title="Interfaces Pendientes por Revisión" total={12} status={StatusOption.PENDING} />
                <CardComponent title="Interfaces Revisadas" total={12} status={StatusOption.REVIEW} />
            </section>
            <section id="description" className="w-full px-4 flex flex-col flex-nowrap">
                <h1 className={`${styles.textTitle} text-3xl font-bold`}>Estadísticas de Usuarios</h1>
                <p className={`${styles.textNormal} text-lg`}>Revise las estadítiscas de asignaciones de los usuarios disponibles.</p>
            </section>
            <section id="statistics-user" className="w-full pb-4 px-4 flex flex-col flex-nowrap gap-4">
                <div className={`${styles.cardStatistics}`}>
                    <section id="title" className="w-full p-2 flex flex-row gap-2">
                        <Image
                            src="/user/icon.svg"
                            alt="user"
                            width={24}
                            height={24}
                        />
                        <h3 className={`${styles.textTitle} text-xl font-bold`}>Usuario 1</h3>
                    </section>
                    <section id="content" className="w-full flex flex-row flex-nowrap gap-20">
                        <div className="flex flex-col flex-nowrap">
                            <div className="w-fit h-fit flex flex-col flex-nowrap">
                                <h3 className={`${styles.textNormal} text-lg font-bold`}>Interfaces Asignadas</h3>
                                <p className={`${styles.textNormal} text-lg`}>12</p>
                            </div>
                            <div className="w-fit h-fit flex flex-col flex-nowrap">
                                <h3 className={`${styles.textNormal} text-lg font-bold`}>Interfaces Asignadas en el Mes</h3>
                                <p className={`${styles.textNormal} text-lg`}>12</p>
                            </div>
                        </div>
                        <div className="flex flex-col flex-nowrap">
                            <div className="w-fit h-fit flex flex-col flex-nowrap">
                                <h3 className={`${styles.textNormal} text-lg font-bold`}>Interfaces Pendientes</h3>
                                <p className={`${styles.textNormal} text-lg`}>12</p>
                            </div>
                            <div className="w-fit h-fit flex flex-col flex-nowrap">
                                <h3 className={`${styles.textNormal} text-lg font-bold`}>Interfaces Pendientes de Hoy</h3>
                                <p className={`${styles.textNormal} text-lg`}>12</p>
                            </div>
                        </div>
                        <div className="flex flex-col flex-nowrap">
                            <div className="w-fit h-fit flex flex-col flex-nowrap">
                                <h3 className={`${styles.textNormal} text-lg font-bold`}>Interfaces Revisadas</h3>
                                <p className={`${styles.textNormal} text-lg`}>12</p>
                            </div>
                            <div className="w-fit h-fit flex flex-col flex-nowrap">
                                <h3 className={`${styles.textNormal} text-lg font-bold`}>Interfaces Revisadas de Hoy</h3>
                                <p className={`${styles.textNormal} text-lg`}>12</p>
                            </div>
                        </div>
                    </section>
                </div>
                <div className={`${styles.cardStatistics}`}>
                    <section id="title" className="w-full p-2 flex flex-row gap-2">
                        <Image
                            src="/user/icon.svg"
                            alt="user"
                            width={24}
                            height={24}
                        />
                        <h3 className={`${styles.textTitle} text-xl font-bold`}>Usuario 1</h3>
                    </section>
                    <section id="content" className="w-full flex flex-row flex-nowrap gap-20">
                        <div className="flex flex-col flex-nowrap">
                            <div className="w-fit h-fit flex flex-col flex-nowrap">
                                <h3 className={`${styles.textNormal} text-lg font-bold`}>Interfaces Asignadas</h3>
                                <p className={`${styles.textNormal} text-lg`}>12</p>
                            </div>
                            <div className="w-fit h-fit flex flex-col flex-nowrap">
                                <h3 className={`${styles.textNormal} text-lg font-bold`}>Interfaces Asignadas en el Mes</h3>
                                <p className={`${styles.textNormal} text-lg`}>12</p>
                            </div>
                        </div>
                        <div className="flex flex-col flex-nowrap">
                            <div className="w-fit h-fit flex flex-col flex-nowrap">
                                <h3 className={`${styles.textNormal} text-lg font-bold`}>Interfaces Pendientes</h3>
                                <p className={`${styles.textNormal} text-lg`}>12</p>
                            </div>
                            <div className="w-fit h-fit flex flex-col flex-nowrap">
                                <h3 className={`${styles.textNormal} text-lg font-bold`}>Interfaces Pendientes de Hoy</h3>
                                <p className={`${styles.textNormal} text-lg`}>12</p>
                            </div>
                        </div>
                        <div className="flex flex-col flex-nowrap">
                            <div className="w-fit h-fit flex flex-col flex-nowrap">
                                <h3 className={`${styles.textNormal} text-lg font-bold`}>Interfaces Revisadas</h3>
                                <p className={`${styles.textNormal} text-lg`}>12</p>
                            </div>
                            <div className="w-fit h-fit flex flex-col flex-nowrap">
                                <h3 className={`${styles.textNormal} text-lg font-bold`}>Interfaces Revisadas de Hoy</h3>
                                <p className={`${styles.textNormal} text-lg`}>12</p>
                            </div>
                        </div>
                    </section>
                </div>
            </section>
        </main>
    );
}