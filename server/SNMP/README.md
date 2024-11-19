# CONSULTS SNMP

In order to monitor the network devices on an ongoing basis, it is necessary to perform SNMP queries on a daily basis. 
This is done by running the `main.sh` file in the crontab. This file performs device queries previously obtained from a file (`devices.csv`).

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
If you have a URL to get the list of network devices in JSON format, you can export the global variable with the URL by calling it `DEVICES`. This way, you can run: `devices.sh` to get the data. Or, alternatively, manually place the URL.

**Example:**
```bash
DEVICES="https://example.com/devices"
```

### crontab
It is necessary to specify the `HOME` variable in the crontab to identify the start path for the correct execution of the script. You may also need to specify the `COMMAND_SNMP` and `COMMAND_PING` commands.

## Functioning
It should be noted that the `devices.csv` file must contain the list of devices to be queried in the format of `IP,community` to work.

> **Note:** Each line in the file must contain only one IP and one community.

The `main.sh` script takes 3 parameters: 
* **Parameter 1:** The line with the declaration of the device to start querying from the `devices.csv` file.
* **Parameter 2:** The line with the declaration of the device to finish querying from the `devices.csv` file.
* **Parameter 3:** Number, letter or string identifying the version of the output.

**Example**
```bash
bash main.sh 0 10 1
```

Running the `main.sh` script will perform queries starting from the first host up to host number 10. The output of the queries will be `SNMP-2024-11-19-19_part_1`, where the number after the word *part* would be parameter 3.


```bash
bash main.sh 11 20 2

OUTPUT: SNMP_2024-11-19_part_2
```