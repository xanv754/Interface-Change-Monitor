import os
from typing import List
from constants import InterfaceType, FilepathConstant
from schemas import RegisterInterfaceBody
from system import UpdaterInterfaceHandler
from utils import Log, format_ifStatus, get_yesterday


class SNMPHandler:
    __folderpath: str

    def __init__(self, filepath: str | None = None):
        if filepath: self.__folderpath = filepath
        else: self.__folderpath = FilepathConstant.SNMP_DATA.value

    def get_consults(self) -> bool:
        """Read an file with the SNMP data and update the interfaces in the database."""
        try:
            data: List[RegisterInterfaceBody] = []
            if os.path.isdir(self.__folderpath):
                files = os.listdir(self.__folderpath)
                for file in files:
                    ip = file.split("_")[0]
                    community = file.split("_")[1]
                    sysname = file.split("_")[2]
                    with open(self.__folderpath + "/" + file, "r") as file:
                        for line in file:
                            line = line.strip()
                            if line:
                                ifIndex = line.split(";")[0].strip()
                                ifName = line.split(";")[1].strip()
                                ifDescr = line.split(";")[2].strip()
                                ifAlias = line.split(";")[3].strip()
                                ifHighSpeed = line.split(";")[4].strip()
                                ifOperStatus = format_ifStatus(line.split(";")[5].strip())
                                ifAdminStatus = format_ifStatus(line.split(";")[6].strip())
                                new_interface = RegisterInterfaceBody(
                                    dateConsult=get_yesterday(),
                                    interfaceType=InterfaceType.NEW.value,
                                    ip=ip,
                                    community=community,
                                    sysname=sysname,
                                    ifIndex=int(ifIndex),
                                    ifName=ifName,
                                    ifDescr=ifDescr,
                                    ifAlias=ifAlias,
                                    ifHighSpeed=int(ifHighSpeed),
                                    ifOperStatus=ifOperStatus,
                                    ifAdminStatus=ifAdminStatus,
                                )
                                data.append(new_interface)
                for new_interface in data:
                    updateController = UpdaterInterfaceHandler(data=new_interface)
                    updateController.update()
            else:
                Log.save(f"Consult SNMP of {get_yesterday()} not found", __file__, Log.warning)
        except Exception as e:
            Log.save(str(e), __file__, Log.error)
            return False
        else:
            return True

    def delete_old_data(self) -> bool:
        """Delete the old data of the SNMP."""
        try:
            if os.path.isdir(self.__folderpath):
                #TODO: delete folder
                pass
        except Exception as e:
            Log.save(str(e), __file__, Log.error)
            return False
        else:
            return True
