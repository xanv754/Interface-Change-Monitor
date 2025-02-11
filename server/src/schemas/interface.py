from enum import Enum


class InterfaceSchema(Enum):
    ID = "id"
    IFINDEX = "ifIndex"
    ID_EQUIPMENT = "idEquipment"
    DATE_CONSULT = "dateConsult"
    IFNAME = "ifName"
    IFDESCR = "ifDescr"
    IFALIAS = "ifAlias"
    IFSPEED = "ifSpeed"
    IFHIGHSPEED = "ifHighSpeed"
    IFPHYSADDRESS = "ifPhysAddress"
    IFTYPE = "ifType"
    IFOPERSTATUS = "ifOperStatus"
    IFADMINSTATUS = "ifAdminStatus"
    IFPROMISCUOUSMODE = "ifPromiscuousMode"
    IFCONNECTORPRESENT = "ifConnectorPresent"
    IFLASTCHECK = "ifLastCheck"