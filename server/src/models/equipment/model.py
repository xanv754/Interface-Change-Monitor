from database import PostgresDatabase, GTABLES, EquipmentSchemaDB
from utils import Log


class EquipmentModel:
    ip: str
    community: str

    def __init__(self, ip: str, community: str):
        self.ip = ip
        self.community = community

    def register(self) -> bool:
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
                (self.ip, self.community, None),
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
