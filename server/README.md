# Requerimientos
## Librerías
Este proyecto contiene un archivo `requirements.txt` con las librerías necesarias para el funcionamiento del proyecto.

## Variables de Entorno
Para poder ejecutar operaciones con la base de datos, es necesario definir la variable de entorno `URI_POSTGRES` con la URI de la base de datos en cualquier archivo de configuración.
- Para entorno de desarrollo: `.env.development`
- Para entorno de producción: `.env.production`
- Para entorno general: `.env`

> *Nota:* Las variables de entorno de desarrollo tiene prioridad sobre las de producción y general. Es recomendable solo definir un archivo de configuración.

## Permisos en el directorio `/var/log`
Para que el sistema pueda crear, borrar, modificar y acceder a los archivos de registro, es necesario definir los permisos para el directorio `/var/log/icm`.