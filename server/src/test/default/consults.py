from os import getcwd, path, remove
from constants import InterfaceType
from schemas import RegisterInterfaceBody
from test import constants as testConstants

class DefaultConsults:
    @staticmethod
    def consult_old() -> RegisterInterfaceBody:
        return RegisterInterfaceBody(
            dateConsult=testConstants.DATE_CONSULT,
            interfaceType=InterfaceType.OLD.value,
            ip=testConstants.IP,
            community=testConstants.COMMUNITY,
            sysname=testConstants.SYSNAME,
            ifIndex=testConstants.IFINDEX,
            ifName="test@ifName",
            ifDescr="test@ifDescr",
            ifAlias="test@ifAlias",
            ifHighSpeed=1000,
            ifOperStatus="UP",
            ifAdminStatus="UP",
        )

    @staticmethod
    def consult_new() -> RegisterInterfaceBody:
        return RegisterInterfaceBody(
            dateConsult=testConstants.DATE_CONSULT_TWO,
            interfaceType=InterfaceType.NEW.value,
            ip=testConstants.IP,
            community=testConstants.COMMUNITY,
            sysname=testConstants.SYSNAME,
            ifIndex=testConstants.IFINDEX,
            ifName="test@ifName2",
            ifDescr="test@ifDescr2",
            ifAlias="test@ifAlias2",
            ifHighSpeed=1002,
            ifOperStatus="UP",
            ifAdminStatus="UP",
        )

    @staticmethod
    def consult_old_with_new_sysname() -> RegisterInterfaceBody:
        return RegisterInterfaceBody(
            dateConsult=testConstants.DATE_CONSULT,
            interfaceType=InterfaceType.NEW.value,
            ip=testConstants.IP,
            community=testConstants.COMMUNITY,
            sysname=testConstants.SYSNAME_TWO,
            ifIndex=testConstants.IFINDEX,
            ifName="test@ifName",
            ifDescr="test@ifDescr",
            ifAlias="test@ifAlias",
            ifHighSpeed=1000,
            ifOperStatus="UP",
            ifAdminStatus="UP",
        )
    
    @staticmethod
    def create_consult_file() -> None:
        filepath = getcwd() + f"/{testConstants.IP}_{testConstants.COMMUNITY}_{testConstants.SYSNAME}"
        DefaultConsults.delete_consult_file()
        with open(filepath, 'w') as file:
            file.write(f"{testConstants.IFINDEX};test@ifName;test@ifDescr;test@ifAlias;1000;UP;UP\n")
            file.close()
        return filepath

    @staticmethod
    def delete_consult_file() -> None:
        filepath = getcwd() + f"/{testConstants.IP}_{testConstants.COMMUNITY}_{testConstants.SYSNAME}"
        if path.exists(filepath):
            remove(filepath)
