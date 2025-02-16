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
