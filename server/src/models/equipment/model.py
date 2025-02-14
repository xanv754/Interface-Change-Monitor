from database import PostgresDatabase, GTABLES, EquipmentSchemaDB
from utils import Log


class EquipmentModel:
    ip: str
    community: str
    sysname: str | None

    def __init__(self, ip: str, community: str, sysname: str | None = None):
        self.ip = ip
        self.community = community
        self.sysname = sysname

    def register(self) -> bool:
        """Register an new equipment in the database. \n
        _Note:_ All the data required by the new equipment is extracted from the constructor.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""INSERT INTO {GTABLES.EQUIPMENT.value} (
                    {EquipmentSchemaDB.IP.value}, 
                    {EquipmentSchemaDB.COMMUNITY.value}, 
                    {EquipmentSchemaDB.SYSNAME.value}
                ) VALUES (%s, %s, %s)""",
                (self.ip, self.community, self.sysname),
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
