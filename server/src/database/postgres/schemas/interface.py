from enum import Enum


class InterfaceSchemaDB(Enum):
    """Names of the columns of the interface table."""

    ID = "id"
    IFINDEX = "ifIndex"
    ID_EQUIPMENT = "idEquipment"
    DATE_CONSULT = "dateConsult"
    INTERFACE_TYPE = "interfaceType"
    IFNAME = "ifName"
    IFDESCR = "ifDescr"
    IFALIAS = "ifAlias"
    IFHIGHSPEED = "ifHighSpeed"
    IFOPERSTATUS = "ifOperStatus"
    IFADMINSTATUS = "ifAdminStatus"
