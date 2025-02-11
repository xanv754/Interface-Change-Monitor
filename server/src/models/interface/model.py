from constants import GTABLES, InterfaceFields
from database import PostgresDatabase


class InterfaceModel:
    ifInder: int
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
                f"INSERT INTO {GTABLES.INTERFACE.value} ({InterfaceFields.IFINDEX.value}, {InterfaceFields.ID_EQUIPMENT.value}, {InterfaceFields.DATE_CONSULT.value}, {InterfaceFields.IFNAME.value}, {InterfaceFields.IFDESCR.value}, {InterfaceFields.IFALIAS.value}, {InterfaceFields.IFSPEED.value}, {InterfaceFields.IFHIGHSPEED.value}, {InterfaceFields.IFPHYSADDRESS.value}, {InterfaceFields.IFTYPE.value}, {InterfaceFields.IFOPERSTATUS.value}, {InterfaceFields.IFADMINSTATUS.value}, {InterfaceFields.IFPROMISCUOUSMODE.value}, {InterfaceFields.IFCONNECTORPRESENT.value}, {InterfaceFields.IFLASTCHECK.value}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
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
