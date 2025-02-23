import os
from datetime import datetime, timedelta
from updater import UpdaterInterfaces
from utils import Log, format_ifStatus

DATE = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
FILEPATH_BASE = os.getcwd().split("src")[0] + "SNMP/data/SNMP_" + DATE
FLAG_DATE = "DATE"
FLAG_EQUIPMENT = ["IP", "Community"]

class SNMP:
    filepath: str

    def __init__(self, filepath: str | None = None):
        if filepath: self.filepath = filepath
        else: self.filepath = FILEPATH_BASE

    def _get_content(self, line: str) -> str:
        """Get the content of the line."""
        content = "EMPTY"
        if (
            "sysName" in line or
            "ifName" in line or
            "ifDescr" in line or
            "ifAlias" in line
        ):
            content = line.split("STRING:")[1].strip()
        elif (
            "ifIndex" in line or
            "ifOperStatus" in line or
            "ifAdminStatus" in line
        ):
            content = line.split("INTEGER:")[1].strip()
        elif ("ifHighSpeed" in line):
            content = line.split("Gauge32:")[1].strip()
        return content

    def get_consults(self) -> bool:
        """Read an file with the SNMP data and update the interfaces in thedatabase."""
        try:
            data = []
            if os.path.exists(self.filepath):
                with open(self.filepath, "r") as file:
                    for line in file:
                        if not FLAG_DATE in line:
                            if not line.split("=")[0] in FLAG_EQUIPMENT:
                                content = self._get_content(line)
                                if "ifAdminStatus" in line or "ifOperStatus" in line:
                                    content = format_ifStatus(content)
                                data.append(content)
                            else:
                                data.append(line.split("=")[1].strip())
                        elif len(data) != 0:
                            updateDB = UpdaterInterfaces(data)
                            updateDB.update()
                if len(data) != 0:
                    updateDB = UpdaterInterfaces(data)
                    updateDB.update()
            else:
                Log.save(f"Consult SNMP of {DATE} not found ({self.filepath})", __file__, Log.warning)
                return True
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False
        else:
            return True
