# Consultas SNMP
Para monitorizar los equipos de red de forma continua, es necesario realizar consultas SNMP diariamente. 
Esto se hace ejecutando el archivo `main.sh` en el crontab. Este archivo realiza las consultas a los equipos previamente obtenidos en un archivo (`devices.csv`).

## Requerimientos
### `consults.sh`
Se debe tener exportada el comando para la ejecución del snmp. De otra forma se debe modificar el script con el comando correcto según el equipo que se pondrá a ejecutar.

**Ejemplo:**
```bash
COMMAND_SNMP="snmpwalk -v 2c -c"
```

### `ping.sh`
se debe tener exportada el comando para la ejecución del ping. De otra forma se debe modificar el script con el comando correcto según el equipo que se pondrá a ejecutar.

**Ejemplo:**
```bash
COMMAND_PING="ping"
```

### `devices.sh`
Si se tiene una URL para obtener la lista de los dispositivos de red en formato JSON, puede exportar la variable global con la URL llamandola `DEVICES`. De esta forma, podrá ejecutar: `devices.sh` para obtener la data. O de otra forma, colocar manualmente la URL.

**Ejemplo:**
```bash
DEVICES="https://example.com/devices"
```

### crontab
Es necesario especificar la variable `HOME` en el crontab para identificar la ruta de inicio para la correcta ejecución del script. Además, de ser necesario, también especificar los comandos `COMMAND_SNMP` y `COMMAND_PING`.

## Funcionamiento
Se debe tener en claro que el archivo `devices.csv` debe tener al lista de equipos a consultar en el formato de: `IP,community` para funcionar.

> **Nota:** Cada línea del archivo debe contener únicamente una IP y una comunidad.

El script `main.sh` recibe 3 parámetros: 
* **Parámetro 1:** La línea con la declaración del equipo que se empezará a consultar del archivo `devices.csv`.
* **Parámetro 2:** La línea con la declaración del equipo que terminará de consultar del archivo `devices.csv`.
* **Parámetro 3:** Número, letra o cadena que identifique versión de la salida

**Ejemplo**
```bash
bash main.sh 0 10 1
```
La ejecución del script `main.sh` realizará consultas a partir del primer equipo hasta el equipo número 10. La salida de las consultas será: `SNMP-2024-11-19_part_1`, donde el número después de la palabra *part* vendría siendo el parámetro 3.

```bash
bash main.sh 11 20 2

SALIDA: SNMP_2024-11-19_part_2
```
