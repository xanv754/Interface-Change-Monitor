# Servidor
El servidor es el encargado de la recopilación de datos de todas las interfaces de la red, así como su almacenamiento y su servicio de API para el cliente.El servidor fue diseñado en Python como lenguaje para la administración de la API, sin embargo, se extrae la información de las interfaces de consultas SNMP realizadas a los equipos mediante scripts en bash, dando como respuesta de las consultas, unos archivos `.json` ubicados en la carpeta `server/api/data`.

### Consultas SNMP
Véase el ejemplo en: [Respuesta consultas SNMP](examples/response_consults.json) para entender la salida de la consulta.

> **Nota**: El proyecto actual no tiene contenido los scripts para consultas SNMP por bash a los equipos por términos de privacidad y confidencialidad. Proporcione su propio script asegurando el resultado de un `.json` o utilice [Repo: Generador JSON por Consultas SNMP](https://github.com/Angxandralol/SNMP-JSON).

### API
El servidor proporciona una API especial para el cliente utilizando [FastAPI](https://fastapi.tiangolo.com/). Para el correcto funcionamiento del sistema, se debe levantar la API corriendo el script `main.py`.

#### Librerias
`requeriments.txt` contiene las librerias necesarias para la correcta compilación del servidor y el levantamiento de la API.

#### Variables de Entorno Requeridas
```
URI="uri-mongodb"
DATABASE="nombre-de-la-base-de-datos"
JWT_SECRET_KEY=""
JWT_ALGORITHM=""
JWT_TOKEN_EXPIRE=
```

#### Actualización del Servidor
> **Importante** Se debe declarar las variables de entornos correctamente antes de la ejecución.

Ejecutar el script `update.py` para la actualización del servidor con la información de las consultas previamente realizadas. 

#### Dockers & Nginx
La API cuenta con su `dockerfile` para construir su imagen, y el proyecto contiene el `docker-compose.yml` para la gestión del servidor y base de datos. El servidor tiene un archivo de configuración nginx para gestión de comunicación si nginx no está instalado en el servidor.