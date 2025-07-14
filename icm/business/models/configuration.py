from pydantic import BaseModel


class ConfigUser(BaseModel):
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


class NewConfigModel(BaseModel):
    can_assign: ConfigUser
    can_receive_assignment: ConfigUser
    view_information_global: ConfigUser
    notification_changes: ConfigInterface
