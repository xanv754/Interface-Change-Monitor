from typing import List
from database import PostgresDatabase, GTABLES, EquipmentSchemaDB
from schemas import EquipmentResponseSchema
from utils import equipment_to_dict, Log


class Equipment:
    id: int | None
    ip: str | None
    community: str | None
    sysname: str | None

    def __init__(
        self,
        id: int | None = None,
        ip: str | None = None,
        community: str | None = None,
        sysname: str | None = None,
    ):
        self.id = id
        self.ip = ip
        self.community = community
        self.sysname = sysname

    @staticmethod
    def get_all() -> List[EquipmentResponseSchema]:
        """Get all equipments of the system."""
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(f"""SELECT * FROM {GTABLES.EQUIPMENT.value}""")
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return equipment_to_dict(result)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    def get_all_by_sysname(self) -> List[EquipmentResponseSchema]:
        """Get all equipments filter by sysname of the equipment. \n
        _Note:_ Its necessary declare the sysname of the equipment in the constructor.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.EQUIPMENT.value}
                WHERE {EquipmentSchemaDB.SYSNAME.value} = %s""",
                (self.sysname,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return equipment_to_dict(result)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    def get_by_id(self) -> EquipmentResponseSchema | None:
        """Get info of the equipment by ID. \n
        _Note:_ Its necessary declare the ID equipment in the constructor.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.EQUIPMENT.value}
                WHERE {EquipmentSchemaDB.ID.value} = %s""",
                (self.id,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            equipment = equipment_to_dict([result])
            return equipment[0]
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    def get_by_ip_community(self) -> EquipmentResponseSchema | None:
        """Get equipment filter by:
        - IP address of the equipment
        - Community of the equipment \n
        _Note:_ Its necessary declare the ip and the community of the equipment in the constructor.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.EQUIPMENT.value}
                WHERE {EquipmentSchemaDB.IP.value} = %s AND
                {EquipmentSchemaDB.COMMUNITY.value} = %s""",
                (self.ip, self.community),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            equipment = equipment_to_dict([result])
            return equipment[0]
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    def get_by_ip_community_sysname(self) -> EquipmentResponseSchema | None:
        """Get equipment filter by:
        - IP address of the equipment
        - Community of the equipment
        - Sysname of the equipment \n
        _Note:_ Its necessary declare the ip, community and sysname of the equipment in the constructor.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.EQUIPMENT.value}
                WHERE {EquipmentSchemaDB.IP.value} = %s AND
                {EquipmentSchemaDB.COMMUNITY.value} = %s AND
                {EquipmentSchemaDB.SYSNAME.value} = %s""",
                (self.ip, self.community, self.sysname),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            equipment = equipment_to_dict([result])
            return equipment[0]
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    def update_sysname(self, sysname: str) -> bool:
        """Update sysname of the equipment. \n
        _Note:_ Its necessary declare the ip and the community of the equipment in the constructor.

        Parameters
        ----------
        sysname : str
            New sysname of the equipment.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""UPDATE {GTABLES.EQUIPMENT.value}
                SET {EquipmentSchemaDB.SYSNAME.value} = %s
                WHERE {EquipmentSchemaDB.IP.value} = %s AND
                {EquipmentSchemaDB.COMMUNITY.value} = %s""",
                (sysname, self.ip, self.community),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False
        else:
            if status and "UPDATE" in status:
                return True
            else:
                return False

    def update_community(self, community: str) -> bool:
        """Update community of the equipment. \n
        _Note:_ Its necessary declare the ID equipment in the constructor.

        Parameters
        ----------
        community : str
            New community of the equipment.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""UPDATE {GTABLES.EQUIPMENT.value}
                SET {EquipmentSchemaDB.COMMUNITY.value} = %s
                WHERE {EquipmentSchemaDB.ID.value} = %s""",
                (community, self.id),
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

    def delete(self) -> bool:
        """Delete the equipment. \n
        _Note:_ Its necessary declare the ID equipment in the constructor.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""DELETE FROM {GTABLES.EQUIPMENT.value}
                WHERE {EquipmentSchemaDB.ID.value} = %s""",
                (self.id,),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False
        else:
            if status and status == "DELETE 1":
                return True
            else:
                return False
