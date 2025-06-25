import styles from './navbar.module.css';

export default function NavbarStandardComponent() {
    return (
        <nav className={styles.nav}>
            <h1>Monitor de Cambios de Interfaces</h1>
            <ul>
                <li><a href="/dashboard/personal">Inicio</a></li>
                <li><a href="/history/personal">Historial</a></li>
                <li><a href="/profile">Perfil</a></li>
                <li><a href="/out">Cerrar Sesión</a></li>
            </ul>
        </nav>
    );
}