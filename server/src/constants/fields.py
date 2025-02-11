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

class OperatorFields(Enum):
    USERNAME = "username"
    NAME = "name"
    LASTNAME = "lastname"
    PASSWORD = "password"
    PROFILE = "profile"
    STATUS_ACCOUNT = "statusaccount"
    CREATED_AT = "createdat"

class AssignmentFields(Enum):
    ID = "id"
    CHANGE_INTERFACE = "changeinterface"
    OLD_INTERFACE = "oldinterface"
    OPERATOR = "operator"
    DATE_ASSIGNMENT = "dateassignment"
    STATUS_ASSIGNMENT = "statusassignment"
    ASSIGNED_BY = "assignedby"
    UPDATED_AT = "updatedat"