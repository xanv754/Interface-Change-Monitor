import styles from './navbar.module.css';

export default function NavbarAdminComponent() {
    return (
        <nav className={styles.nav}>
            <h1>Monitor de Cambios de Interfaces</h1>
            <ul>
                <li><a href="/dashboard/admin">Inicio</a></li>
                <li><a href="/history/admin">Historial</a></li>
                <li><a href="/statistics">Estadísticas</a></li>
                <li><a href="/settings">Configuración</a></li>
                <li><a href="/profile">Perfil</a></li>
                <li><a href="/out">Cerrar Sesión</a></li>
            </ul>
        </nav>
    );
}