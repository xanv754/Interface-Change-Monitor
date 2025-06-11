# Requerimientos
## Librerías
Este proyecto contiene un archivo `requirements.txt` con las librerías necesarias para el funcionamiento del proyecto.

## Variables de Entorno
**`URI_POSTGRES`**
Para poder ejecutar operaciones con la base de datos, es necesario definir la variable de entorno `URI_POSTGRES` con la URI de la base de datos en cualquier archivo de configuración.
- Para entorno de desarrollo: `.env.development`
- Para entorno de producción: `.env.production`
- Para entorno de pruebas unitarias: `.env.test`
- Para entorno general: `.env`

> *Nota:* Las variables de entorno de desarrollo tiene prioridad sobre las de producción y general. Es recomendable solo definir un archivo de configuración.

**`SECRET_KEY`**
Para poder ejecutar operaciones con el servidor, es necesario definir la variable de entorno `SECRET_KEY` con una clave secreta en cualquier archivo de configuración.

Puedes generar una clave secreta con el siguiente comando:
```bash
openssl rand -hex 32
```

## Permisos en el directorio `/var/log`
Para que el sistema pueda crear, borrar, modificar y acceder a los archivos de registro, es necesario definir los permisos para el directorio `/var/log/icm`.

# Ejecución
## Modo desarrollo
Para ejecutar el servidor en modo desarrollo, ejecuta el siguiente comando:
```bash
fastapi dev api/app.py
```