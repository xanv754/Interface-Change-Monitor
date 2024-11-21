from datetime import datetime
from pydantic import BaseModel
from database.constants.date import TypeDate
from database.constants.status import TypeStatus

class InterfaceEntity(BaseModel):
    id: int
    ifIndex: int
    idEquipment: int
    dateConsult: datetime
    dateType: TypeDate
    ifName: str
    ifDescr: str
    ifAlias: str
    ifSpeed: int
    ifHighSpeed: int
    ifPhysAddress: str
    ifType: str
    ifOperStatus: TypeStatus
    ifAdminStatus: TypeStatus
    ifPromiscuousMode: bool
    ifConnectorPresent: bool
    ifLastCheck: str