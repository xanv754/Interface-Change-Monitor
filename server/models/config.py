from pydantic import BaseModel


class ConfigField:
    SNMP = "snmp"
    HOST = "host"
    USER = "user"
    PASSWORD = "password"
    PORT = "port"
    CAN_ASSIGN = "can_assign"
    CAN_RECEIVE_ASSIGNMENT = "can_receive_assignment"
    VIEW_INFORMATION_GLOBAL = "view_information_global"
    NOTIFICATION_CHANGES = "notification_changes"
    ROOT = "root"
    USER = "user"
    SOPORT = "soport"
    ADMIN = "admin"
    IFNAME = "ifName"
    IFDESCR = "ifDescr"
    IFALIAS = "ifAlias"
    IFHIGHSPEED = "ifHighSpeed"
    IFOPERSTATUS = "ifOperStatus"
    IFADMINSTATUS = "ifAdminStatus"

class ConfigSnmp(BaseModel):
    host: str
    user: str
    password: str
    port: int


class ConfigUsers(BaseModel):
    root: bool
    admin: bool
    user: bool
    soport: bool


class ConfigInterface(BaseModel):
    ifName: bool
    ifDescr: bool
    ifAlias: bool
    ifHighSpeed: bool
    ifOperStatus: bool
    ifAdminStatus: bool


class ConfigModel(BaseModel):
    snmp: ConfigSnmp
    can_assign: ConfigUsers
    can_receive_assignment: ConfigUsers
    view_information_global: ConfigUsers
    notification_changes: ConfigInterface