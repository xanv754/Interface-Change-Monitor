from constants import GTABLES
from database import PostgresDatabase
from schemas import InterfaceSchema


class InterfaceModel:
    ifIndex: int
    idEquipment: int
    dateConsult: str
    ifName: str
    ifDescr: str
    ifAlias: str
    ifSpeed: int
    ifHighSpeed: int
    ifPhysAddress: str
    ifType: str
    ifOperStatus: str
    ifAdminStatus: str
    ifPromiscuousMode: bool
    ifConnectorPresent: bool
    ifLastCheck: str

    def __init__(
        self,
        ifIndex: int,
        idEquipment: int,
        dateConsult: str,
        ifName: str,
        ifDescr: str,
        ifAlias: str,
        ifSpeed: int,
        ifHighSpeed: int,
        ifPhysAddress: str,
        ifType: str,
        ifOperStatus: str,
        ifAdminStatus: str,
        ifPromiscuousMode: bool,
        ifConnectorPresent: bool,
        ifLastCheck: str,
    ):
        self.ifIndex = ifIndex
        self.idEquipment = idEquipment
        self.dateConsult = dateConsult
        self.ifName = ifName
        self.ifDescr = ifDescr
        self.ifAlias = ifAlias
        self.ifSpeed = ifSpeed
        self.ifHighSpeed = ifHighSpeed
        self.ifPhysAddress = ifPhysAddress
        self.ifType = ifType
        self.ifOperStatus = ifOperStatus.upper()
        self.ifAdminStatus = ifAdminStatus.upper()
        self.ifPromiscuousMode = ifPromiscuousMode
        self.ifConnectorPresent = ifConnectorPresent
        self.ifLastCheck = ifLastCheck

    def register(self) -> bool:
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"INSERT INTO {GTABLES.INTERFACE.value} ({InterfaceSchema.IFINDEX.value}, {InterfaceSchema.ID_EQUIPMENT.value}, {InterfaceSchema.DATE_CONSULT.value}, {InterfaceSchema.IFNAME.value}, {InterfaceSchema.IFDESCR.value}, {InterfaceSchema.IFALIAS.value}, {InterfaceSchema.IFSPEED.value}, {InterfaceSchema.IFHIGHSPEED.value}, {InterfaceSchema.IFPHYSADDRESS.value}, {InterfaceSchema.IFTYPE.value}, {InterfaceSchema.IFOPERSTATUS.value}, {InterfaceSchema.IFADMINSTATUS.value}, {InterfaceSchema.IFPROMISCUOUSMODE.value}, {InterfaceSchema.IFCONNECTORPRESENT.value}, {InterfaceSchema.IFLASTCHECK.value}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    self.ifIndex,
                    self.idEquipment,
                    self.dateConsult,
                    self.ifName,
                    self.ifDescr,
                    self.ifAlias,
                    self.ifSpeed,
                    self.ifHighSpeed,
                    self.ifPhysAddress,
                    self.ifType,
                    self.ifOperStatus,
                    self.ifAdminStatus,
                    self.ifPromiscuousMode,
                    self.ifConnectorPresent,
                    self.ifLastCheck,
                ),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            print(e)
            return False
        else:
            if status and status == "INSERT 0 1":
                return True
            else:
                return False
