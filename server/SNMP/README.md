# CONSULTS SNMP

In order to monitor the network devices on an ongoing basis, it is necessary to perform SNMP queries on a daily basis. 
This is done by running the `main.sh` file in the crontab.

## Requirements
### `consults.sh`
Must be exported with the command for SNMP execution. Otherwise, the script must be modified with the correct command according to the equipment to be executed.

**Example:**
```bash
COMMAND_SNMP="snmpwalk -v 2c -c"
```

### `ping.sh`
Must be exported with the command for ping execution. Otherwise, the script must be modified with the correct command according to the equipment to be executed.

**Example:**
```bash
COMMAND_PING="ping"
```

### `devices.sh`
If you have a URL to get the list of network devices in JSON format, you can export the global variable with the URL by calling it `DEVICES`. This way, you can run: `devices.sh` to get the data.

**Example:**
```bash
DEVICES="https://example.com/devices"
```
