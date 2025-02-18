from os import getcwd, path, remove
from test import constants

class DefaultConsults:
    @staticmethod
    def consult_old() -> list:
        consult = [
            constants.IP,
            constants.COMMUNITY,
            constants.SYSNAME,
            constants.IFINDEX,
            "test@ifName",
            "test@ifDescr",
            "test@ifAlias",
            1000,
            1000,
            "test@ifPhysAddress",
            "test@ifType",
            "UP",
            "UP",
            False,
            False,
            constants.DATE_ALTERNATIVE,
        ]
        return consult
    
    @staticmethod
    def consult_new() -> list:
        consult = [
            constants.IP,
            constants.COMMUNITY,
            constants.SYSNAME,
            constants.IFINDEX,
            "test@ifName2",
            "test@ifDescr2",
            "test@ifAlias2",
            1002,
            1002,
            "test@ifPhysAddress",
            "test@ifType",
            "UP",
            "UP",
            False,
            False,
            constants.DATE_CONSULT_TWO,
        ]
        return consult

    @staticmethod
    def consult_old_with_new_sysname() -> list:
        consult = [
            constants.IP,
            constants.COMMUNITY,
            constants.SYSNAME_TWO,
            constants.IFINDEX,
            "test@ifName",
            "test@ifDescr",
            "test@ifAlias",
            1000,
            1000,
            "test@ifPhysAddress",
            "test@ifType",
            "UP",
            "UP",
            False,
            False,
            constants.DATE_ALTERNATIVE,
        ]
        return consult

    @staticmethod
    def create_consult_file() -> None:
        filepath = getcwd() + "/example-consult"
        DefaultConsults.delete_consult_file()
        with open(filepath, "w") as file:
            file.write("DATE=2025-01-01\n")
            file.write("IP=192.168.1.1\n")
            file.write("Community=public\n")
            file.write("SNMPv2-MIB::sysName.0 = STRING: test@Sysname\n")
            file.write("IF-MIB::ifIndex.1 = INTEGER: 1\n")
            file.write("IF-MIB::ifName.1 = STRING: test@ifName\n")
            file.write("IF-MIB::ifDescr.1 = STRING: test@ifDescr\n")
            file.write("IF-MIB::ifAlias.1 = STRING: test@ifAlias\n")
            file.write("IF-MIB::ifSpeed.1 = Gauge32: 1000\n")
            file.write("IF-MIB::ifHighSpeed.1 = Gauge32: 1000\n")
            file.write("IF-MIB::ifPhysAddress.1 = STRING: cc:cc:cc:cc:cc:cc\n")
            file.write("IF-MIB::ifType.1 = INTEGER: mpls(166)\n")
            file.write("IF-MIB::ifOperStatus.1 = INTEGER: up(1)\n")
            file.write("IF-MIB::ifAdminStatus.1 = INTEGER: up(1)\n")
            file.write("IF-MIB::ifPromiscuousMode.1 = INTEGER: false(2)\n")
            file.write("IF-MIB::ifConnectorPresent.1 = INTEGER: false(2)\n")
            file.write("IF-MIB::ifLastChange.1 = Timeticks: (123456789) 0:00:00.00\n")
            file.close()
        return filepath
    
    @staticmethod
    def delete_consult_file() -> None:
        filepath = getcwd() + "/example-consult"
        if path.exists(filepath):
            remove(filepath)