from constants import InterfaceType
from database import PostgresDatabase, GTABLES, InterfaceSchemaDB
from utils import Log


class InterfaceModel:
    id: int | None
    ifIndex: int | None
    idEquipment: int | None
    dateConsult: str
    interfaceType: str
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
        ifIndex: int | None = None,
        idEquipment: int | None = None,
        interfaceType: str = InterfaceType.NEW.value,
        id: int | None = None,
    ):
        self.id = id
        self.ifIndex = ifIndex
        self.idEquipment = idEquipment
        self.dateConsult = dateConsult
        self.interfaceType = interfaceType
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
                f"""INSERT INTO {GTABLES.INTERFACE.value} (
                    {InterfaceSchemaDB.IFINDEX.value}, 
                    {InterfaceSchemaDB.ID_EQUIPMENT.value}, 
                    {InterfaceSchemaDB.DATE_CONSULT.value}, 
                    {InterfaceSchemaDB.INTERFACE_TYPE.value},
                    {InterfaceSchemaDB.IFNAME.value}, 
                    {InterfaceSchemaDB.IFDESCR.value}, 
                    {InterfaceSchemaDB.IFALIAS.value}, 
                    {InterfaceSchemaDB.IFSPEED.value}, 
                    {InterfaceSchemaDB.IFHIGHSPEED.value}, 
                    {InterfaceSchemaDB.IFPHYSADDRESS.value}, 
                    {InterfaceSchemaDB.IFTYPE.value}, 
                    {InterfaceSchemaDB.IFOPERSTATUS.value}, 
                    {InterfaceSchemaDB.IFADMINSTATUS.value}, 
                    {InterfaceSchemaDB.IFPROMISCUOUSMODE.value}, 
                    {InterfaceSchemaDB.IFCONNECTORPRESENT.value}, 
                    {InterfaceSchemaDB.IFLASTCHECK.value}
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    self.ifIndex,
                    self.idEquipment,
                    self.dateConsult,
                    self.interfaceType,
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
            Log.save(e, __file__, Log.error)
            return False
        else:
            if status and status == "INSERT 0 1":
                return True
            else:
                return False

    def update(self) -> bool:
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""UPDATE {GTABLES.INTERFACE.value} 
                SET {InterfaceSchemaDB.DATE_CONSULT.value} = %s,
                {InterfaceSchemaDB.IFNAME.value} = %s, 
                {InterfaceSchemaDB.IFDESCR.value} = %s, 
                {InterfaceSchemaDB.IFALIAS.value} = %s, 
                {InterfaceSchemaDB.IFSPEED.value} = %s, 
                {InterfaceSchemaDB.IFHIGHSPEED.value} = %s, 
                {InterfaceSchemaDB.IFPHYSADDRESS.value} = %s, 
                {InterfaceSchemaDB.IFTYPE.value} = %s, 
                {InterfaceSchemaDB.IFOPERSTATUS.value} = %s, 
                {InterfaceSchemaDB.IFADMINSTATUS.value} = %s, 
                {InterfaceSchemaDB.IFPROMISCUOUSMODE.value} = %s, 
                {InterfaceSchemaDB.IFCONNECTORPRESENT.value} = %s, 
                {InterfaceSchemaDB.IFLASTCHECK.value} = %s 
                WHERE {InterfaceSchemaDB.ID.value} = %s""",
                (
                    self.dateConsult,
                    self.ifName,
                    self.ifDescr,
                    self.ifAlias,
                    self.ifSpeed,
                    self.ifHighSpeed,
                    self.ifPhysAddress,
                    self.ifType,
                    self.ifOperStatus.upper(),
                    self.ifAdminStatus.upper(),
                    self.ifPromiscuousMode,
                    self.ifConnectorPresent,
                    self.ifLastCheck,
                    self.id,
                ),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False
        else:
            if status and status == "UPDATE 1":
                return True
            else:
                return False
