from enum import Enum


class EquipmentFields(Enum):
    ID = "id"
    IP = "ip"
    COMMUNITY = "community"
    SYSNAME = "sysname"
    CREATED_AT = "createdat"
    UPDATED_AT = "updatedat"

class InterfaceFields(Enum):
    ID = "id"
    IFINDEX = "ifIndex"
    IDEQUIPMENT = "idEquipment"
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
