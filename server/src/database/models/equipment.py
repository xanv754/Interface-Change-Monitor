from typing import List
from database.constants.tables import Tables as GTABLES # Global Tables
from database.database import PostgresDatabase
from database.schemas.equipment import EquipmentSchemaDB
from schemas.equipment import EquipmentSchema
from utils.convert import EquipmentResponse
from utils.log import LogHandler


class EquipmentModel:
    """Model for all queries of the equipment table."""

    @staticmethod
    def register(ip: str, community: str, sysname: str | None) -> bool:
        """Register an new equipment in the database.

        Parameters
        ----------
        ip : str
            Equipment's IP.
        community : str
            Equipment's community.
        sysname : str
            Equipment's sysname.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    INSERT INTO {GTABLES.EQUIPMENT.value} (
                        {EquipmentSchemaDB.IP.value},
                        {EquipmentSchemaDB.COMMUNITY.value},
                        {EquipmentSchemaDB.SYSNAME.value}
                    ) VALUES (%s, %s, %s)
                """,
                (ip, community, sysname),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if status and status == "INSERT 0 1":
                return True
            else:
                return False

    @staticmethod
    def get_by_id(id: int) -> EquipmentSchema | None:
        """Get info of the equipment by ID.

        Parameters
        ----------
        id : int
            Equipment's ID.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT *
                    FROM
                        {GTABLES.EQUIPMENT.value}
                    WHERE
                        {EquipmentSchemaDB.ID.value} = %s
                """,
                (id,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            return EquipmentResponse.convert_to_dict([result])[0]
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_by_info(ip: str, community: str) -> EquipmentSchema | None:
        """Get equipment filter by:
            - IP address of the equipment.
            - Community of the equipment.

        Parameters
        ----------
        ip : str
            Equipment's IP.
        communtiy : str
            Equipment's community.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT *
                    FROM
                        {GTABLES.EQUIPMENT.value}
                    WHERE
                        {EquipmentSchemaDB.IP.value} = %s AND
                        {EquipmentSchemaDB.COMMUNITY.value} = %s
                """,
                (ip, community),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            return EquipmentResponse.convert_to_dict([result])[0]
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_by_info_sysname(ip: str, community: str, sysname: str) -> EquipmentSchema | None:
        """Get equipment filter by:
            - IP address of the equipment
            - Community of the equipment
            - Sysname of the equipment.

        Parameters
        ----------
        ip : str
            Equipment's IP.
        communtiy : str
            Equipment's community.
        sysname : str
            Equipment's sysname.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT *
                    FROM
                        {GTABLES.EQUIPMENT.value}
                    WHERE
                    {EquipmentSchemaDB.IP.value} = %s AND
                    {EquipmentSchemaDB.COMMUNITY.value} = %s AND
                    {EquipmentSchemaDB.SYSNAME.value} = %s
                """,
                (ip, community, sysname),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            return EquipmentResponse.convert_to_dict([result])[0]
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_all() -> List[EquipmentSchema]:
        """Get all equipments in the database."""
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT *
                    FROM
                        {GTABLES.EQUIPMENT.value}
                """
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return EquipmentResponse.convert_to_dict(result)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def update_sysname(ip: str, community: str, sysname: str) -> bool:
        """Update sysname of the equipment.
        Parameters
        ----------
        ip : str
            Equipment's IP.
        communtiy : str
            Equipment's community.
        sysname : str
            Equipment's sysname.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    UPDATE
                        {GTABLES.EQUIPMENT.value}
                    SET
                        {EquipmentSchemaDB.SYSNAME.value} = %s
                    WHERE
                        {EquipmentSchemaDB.IP.value} = %s AND
                        {EquipmentSchemaDB.COMMUNITY.value} = %s
                """,
                (sysname, ip, community),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if status and "UPDATE" in status:
                return True
            else:
                return False

    @staticmethod
    def update_community(id: int, community: str) -> bool:
        """Update community of the equipment.

        Parameters
        ----------
        id : int
            Equipment's ID.
        community : str
            New community of the equipment.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    UPDATE
                        {GTABLES.EQUIPMENT.value}
                    SET
                        {EquipmentSchemaDB.COMMUNITY.value} = %s
                    WHERE
                        {EquipmentSchemaDB.ID.value} = %s
                """,
                (community, id),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if status and status == "UPDATE 1":
                return True
            else:
                return False

    @staticmethod
    def delete(id: int) -> bool:
        """Delete the equipment.

        Parameters
        ----------
        id : int
            Equipment's ID.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    DELETE FROM
                        {GTABLES.EQUIPMENT.value}
                    WHERE
                        {EquipmentSchemaDB.ID.value} = %s
                """,
                (id,),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if status and status == "DELETE 1":
                return True
            else:
                return False
