# Consultas SNMP
Para monitorizar los equipos de red de forma continua, es necesario realizar consultas SNMP diariamente. 
Esto se hace ejecutando el archivo `main.sh` en el crontab.

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
Si se tiene una URL para obtener la lista de los dispositivos de red en formato JSON, puede exportar la variable global con la URL llamandola `DEVICES`. De esta forma, podrá ejecutar: `devices.sh` para obtener la data.

**Ejemplo:**
```bash
DEVICES="https://example.com/devices"
```