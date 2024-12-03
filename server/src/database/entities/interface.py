from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from database.constants.types.interface import Date, Status

class InterfaceField(Enum):
    id = "id" 
    ifIndex = "ifIndex" 
    idEquipment = "idEquipment" 
    dateConsult = "dateConsult"
    dateType = "dateType" 
    ifName = "ifName"
    ifDescr = "ifDescr"
    ifAlias = "ifAlias"
    ifSpeed = "ifSpeed" 
    ifHighSpeed = "ifHighSpeed" 
    ifPhysAddress = "ifPhysAddress"
    ifType = "ifType"
    ifOperStatus = "ifOperStatus" 
    ifAdminStatus = "ifAdminStatus" 
    ifPromiscuousMode = "ifPromiscuousMode"
    ifConnectorPresent = "ifConnectorPresent"
    ifLastCheck = "ifLastCheck"

class InterfaceEntity(BaseModel):
    id: int
    ifIndex: int
    idEquipment: int
    dateConsult: datetime
    dateType: Date
    ifName: str
    ifDescr: str
    ifAlias: str
    ifSpeed: int
    ifHighSpeed: int
    ifPhysAddress: str
    ifType: str
    ifOperStatus: Status
    ifAdminStatus: Status
    ifPromiscuousMode: bool
    ifConnectorPresent: bool
    ifLastCheck: str