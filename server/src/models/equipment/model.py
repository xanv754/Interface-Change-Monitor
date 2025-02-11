from constants import GTABLES
from database import PostgresDatabase, errors
from schemas import EquipmentSchema


class EquipmentModel:
    ip: str
    community: str
    sysname: str

    def __init__(self, ip: str, community: str, sysname: str):
        self.ip = ip
        self.community = community
        self.sysname = sysname

    def register(self) -> bool:
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""INSERT INTO {GTABLES.EQUIPMENT.value} (
                    {EquipmentSchema.IP.value}, 
                    {EquipmentSchema.COMMUNITY.value}, 
                    {EquipmentSchema.SYSNAME.value}
                ) VALUES (%s, %s, %s)""",
                (self.ip, self.community, self.sysname),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except errors.UniqueViolation:
            print("Error: Equipment already exists")
            return False
        except Exception as e:
            print(e)
            return False
        else:
            if status and status == "INSERT 0 1":
                return True
            else:
                return False
