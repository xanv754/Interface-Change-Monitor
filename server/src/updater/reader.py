import os
from datetime import datetime, timedelta
from updater.load import UpdaterDatabase

DATE = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
FILEPATH = os.getcwd().split("src")[0] + "SNMP/data/" + DATE + ".txt"
FLAG_DATE = "DATE"
FLAG_EQUIPMENT = ["IP", "COMMUNITY", "sysname"]


def reader():
    data = []
    with open(FILEPATH, "r") as file:
        for line in file:
            if not FLAG_DATE in line:
                if not line.split("=")[0] in FLAG_EQUIPMENT:
                    data.append(line.split(":")[3].strip())
                else:
                    data.append(line.split("=")[1].strip())
            elif len(data) != 0:
                updateDB = UpdaterDatabase(data)
                updateDB.update()
    if len(data) != 0:
        updateDB = UpdaterDatabase(data)
        updateDB.update()
