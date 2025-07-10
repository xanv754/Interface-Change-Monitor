# Interface Change Monitor - Monitor de Cambios de Interfaces
Un sistema diseñado para el monitoreo de cambios en las interfaces de dispositivos en una red.

# Índice
--------------------------------------------------------------------------------------------------

# Documentación
Para ver los diagramas de este proyecto, consuta la [documentación]().


# Requisitos
Para ejecutar el proyecto, se requiere tener instalados los siguientes paquetes:
- Python 3.13
- Node.js 24.0
- NPM 11.3
- PM2 6.0

## Variables de Entorno
Para poder ejecutar operaciones con la base de datos, es necesario definir la variable de entorno `URI_POSTGRES` en el archivo variables de entorno de nuestra preferencia `.env.production` o `.env`:
```bash
URI_POSTGRES="postgresql://usuario:contraseña@host:puerto/base_de_datos"
```
> *Nota*: Para ejecutar las **pruebas unitarias** es necesario un archivo `.env.test` con las variables de entorno. Si se desea trabajar en el **entorno de desarrollo**, se debe usar el archivo `.env.development`, que tiene un privilegio de uso antes que el archivo `.env.production` o `.env`. El sistema diferencia el **entorno de desarrollo** entre el **entorno de pruebas**.

Además de esto, para poder ejecutar operaciones con el servidor, es necesario definir la variable de entorno `SECRET_KEY` en el archivo variables de entorno de nuestra preferencia `.env.production` o `.env`:
```bash
SECRET_KEY="clave_secreta"
```

Para generar una clave secreta, puede ejecutar el siguiente comando:
```bash
openssl rand -hex 32
```


# Instalación
Este proyecto es un monorepo, por lo que se debe instalar los paquetes para el frontend y el backend del sistema. Este sistema cuenta con un Makefile para facilitar la instalación y la configuración del sistema. Para inicializar el sistema, ejecuta el siguiente comando:
```bash
make setup
```

También es posible realizar la instalación manualmente siguiendo estos pasos después de tener un entorno virtual activado:
```bash
pip install -e .
cd presentation && npm install
cd presentation && npm run build
pm2 start ecosystem.config.js
```

## Logs
El sistema cuenta con un archivo de registro de cada operación realizada por el backend que se encuentra en el directorio `data/logs`.


# Ejecución
Una vez instaladas con éxito todas las dependencias del sistema, para levantar el sistema, puede ejecutar la siguiente comando:
```bash
make start
```
o 
```bash
pm2 start ecosystem.config.js
```

O si prefiere, puede levantar los servicios manualmente siguiendo estos pasos:
```bash
fastapi run icm/business/api/app.py
cd presentation && npm run start
```

# Mantenimiento
El objetivo del sistema es consultar todas las interfaces de los dispositivos en una red y quedarse con la información de cada una de las interfaces para su comparación de información. De esta forma, el sistema detecta cambios en las interfaces para generar los alertas en el sistema. 

Para que el sistema pueda saber qué interfaces debe consultar, se debe definir un archivo `.csv` con la información de las interfaces que se desea monitorear. Este archivo se debe ubicar en el directorio `data/sources`. El archivo no debe tener encabezados y debe contar con las siguiente informaciones separados por comas:
```bash
IP,COMMUNITY
```
> *Nota*: Todos los equipos declarados en este archivo deben estar dentro de la red para su correcta consulta.

# Configuración del Sistema
Al iniciar el sistema, este crea automáticamente un archivo llamado `system.json`. Este archivo contiene la configuración del sistema para los permisos de usuarios y alertas de las consultas. Además de esto, en este archivo se debe configurar la información del equipo para conectarse mediante SSH para realizar las consultas SNMP.

*Vista del `system.json` creado por defecto*:
```json
{
    "snmp": {
        "host": "127.0.0.1",
        "user": "public",
        "password": "public",
        "port": 22
    },
    "can_assign": {
        "root": true,
        "admin": true,
        "user": false,
        "soport": false
    },
    "can_receive_assignment": {
        "root": false,
        "admin": true,
        "user": true,
        "soport": false
    },
    "view_information_global": {
        "root": true,
        "admin": true,
        "user": false,
        "soport": true
    },
    "notification_changes": {
        "ifName": true,
        "ifDescr": true,
        "ifAlias": true,
        "ifHighSpeed": true,
        "ifOperStatus": false,
        "ifAdminStatus": false
    }
}
```
> *Nota*: El sistema siempre generará automáticamente este archivo si no lo encuentra.
