from typing import List
from psycopg2 import sql
from constants import StatusAssignmentType
from database import (
    GTABLES,
    PostgresDatabase,
    AssignmentSchemaDB,
    InterfaceSchemaDB,
    EquipmentSchemaDB,
    OperatorSchemaDB
)
from schemas import (
    AssignmentSchema,
    AssignmentInterfaceSchema,
    AssignmentStatisticsOperatorSchema,
    AssignmentInterfaceAssignedSchema,
    AssignmentStatisticsSchema
)
from utils import Log, AssignmentResponse



class Assignment:
    id: int
    id_change_interface: int
    id_old_interface: int
    operator: str

    def __init__(
        self,
        id: int | None = None,
        id_new_interface: int | None = None,
        id_old_interface: int | None = None,
        operator: str | None = None,
    ):
        self.id = id
        if operator: self.operator = operator.lower()
        else: self.operator = operator
        self.id_change_interface = id_new_interface
        self.id_old_interface = id_old_interface

    @staticmethod
    def get_statistics_general_by_day(day: str) -> AssignmentStatisticsSchema | None:
        """Get the total number of pending and revised assignments in the database by a day."""
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT
                    COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_pending_assignments,
                    COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} <> '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_revised_assignments
                FROM {GTABLES.ASSIGNMENT.value} a
                WHERE a.{AssignmentSchemaDB.DATE_ASSIGNMENT.value} = %s
                """,
                (day,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            return AssignmentResponse.convert_to_dict_statistics_version(result)
        except Exception as e:
            Log.save(str(e), __file__, Log.error)
            return None

    @staticmethod
    def get_statistics_general_by_month(month: int) -> AssignmentStatisticsSchema | None:
        """Get the total number of pending and revised assignments in the database by a month."""
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT
                    COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_pending_assignments,
                    COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} <> '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_revised_assignments
                FROM {GTABLES.ASSIGNMENT.value} a
                WHERE EXTRACT(MONTH FROM a.{AssignmentSchemaDB.DATE_ASSIGNMENT.value}) = %s
                """,
                (month,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            return AssignmentResponse.convert_to_dict_statistics_version(result)
        except Exception as e:
            Log.save(str(e), __file__, Log.error)
            return None

    @staticmethod
    def get_statistics_assignments_general() -> List[AssignmentStatisticsOperatorSchema]:
        """Get the total number of pending and revised assignments of
        all operators in the database."""
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT
                    o.{OperatorSchemaDB.USERNAME.value} AS username,
                    o.{OperatorSchemaDB.NAME.value} AS name,
                    o.{OperatorSchemaDB.LASTNAME.value} AS lastname,
                    COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_pending_assignments,
                    COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} <> '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_revised_assignments
                FROM {GTABLES.OPERATOR.value} o
                LEFT JOIN
                    {GTABLES.ASSIGNMENT.value} a ON o.{OperatorSchemaDB.USERNAME.value} = a.{AssignmentSchemaDB.OPERATOR.value}
                GROUP BY
                    o.{OperatorSchemaDB.USERNAME.value}
                """
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return AssignmentResponse.convert_to_dict_operator_statistics_version(result)
        except Exception as e:
            Log.save(str(e), __file__, Log.error)
            return []

    @staticmethod
    def get_statistics_assignments_general_by_day(day: str) -> List[AssignmentStatisticsOperatorSchema]:
        """Get the total number of pending and revised assignments of
        all operators on the day in the database.

        Parameters
        -----------
        day : str
            Day to get the statistics.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT
                    o.{OperatorSchemaDB.USERNAME.value} AS username,
                    o.{OperatorSchemaDB.NAME.value} AS name,
                    o.{OperatorSchemaDB.LASTNAME.value} AS lastname,
                    COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_pending_assignments,
                    COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} <> '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_revised_assignments
                FROM {GTABLES.OPERATOR.value} o
                LEFT JOIN
                    {GTABLES.ASSIGNMENT.value} a ON o.{OperatorSchemaDB.USERNAME.value} = a.{AssignmentSchemaDB.OPERATOR.value}
                WHERE
                    a.{AssignmentSchemaDB.DATE_ASSIGNMENT.value} = %s
                GROUP BY
                    o.{OperatorSchemaDB.USERNAME.value}
                """,
                (day,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return AssignmentResponse.convert_to_dict_operator_statistics_version(result)
        except Exception as e:
            Log.save(str(e), __file__, Log.error)
            return []

    @staticmethod
    def get_statistics_assignments_general_by_month(month: int) -> List[AssignmentStatisticsOperatorSchema]:
        """Get the total number of pending and revised assignments of
        all operators on the month in the database.

        Parameters
        -----------
        month : int
            Month to get the statistics.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT
                    o.{OperatorSchemaDB.USERNAME.value} AS username,
                    o.{OperatorSchemaDB.NAME.value} AS name,
                    o.{OperatorSchemaDB.LASTNAME.value} AS lastname,
                    COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_pending_assignments,
                    COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} <> '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_revised_assignments
                FROM {GTABLES.OPERATOR.value} o
                LEFT JOIN
                    {GTABLES.ASSIGNMENT.value} a ON o.{OperatorSchemaDB.USERNAME.value} = a.{AssignmentSchemaDB.OPERATOR.value}
                WHERE
                    EXTRACT(MONTH FROM a.{AssignmentSchemaDB.DATE_ASSIGNMENT.value}) = %s
                GROUP BY
                    o.{OperatorSchemaDB.USERNAME.value}
                """,
                (month,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return AssignmentResponse.convert_to_dict_operator_statistics_version(result)
        except Exception as e:
            Log.save(str(e), __file__, Log.error)
            return []

    @staticmethod
    def get_all_info_assignments_revised_by_month(month: int) -> List[AssignmentInterfaceAssignedSchema]:
        """Get all revised assignments by a month.

        Parameters
        ----------
        month : int
            Month to get the assignments revised.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT
                    a.{AssignmentSchemaDB.ID.value} AS idAssignment,
                    a.{AssignmentSchemaDB.DATE_ASSIGNMENT.value},
                    a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value},
                    a.{AssignmentSchemaDB.ASSIGNED_BY.value},
                    a.{AssignmentSchemaDB.UPDATED_AT.value},
                    oldInterface.{InterfaceSchemaDB.IFNAME.value} AS oldIfName,
                    oldInterface.{InterfaceSchemaDB.IFDESCR.value} AS oldIfDescr,
                    oldInterface.{InterfaceSchemaDB.IFALIAS.value} AS oldIfAlias,
                    oldInterface.{InterfaceSchemaDB.IFHIGHSPEED.value} AS oldIfHighSpeed,
                    oldInterface.{InterfaceSchemaDB.IFOPERSTATUS.value} AS oldIfOperStatus,
                    oldInterface.{InterfaceSchemaDB.IFADMINSTATUS.value} AS oldIfAdminStatus,
                    newInterface.{InterfaceSchemaDB.IFNAME.value} AS newIfName,
                    newInterface.{InterfaceSchemaDB.IFDESCR.value} AS newIfDescr,
                    newInterface.{InterfaceSchemaDB.IFALIAS.value} AS newIfAlias,
                    newInterface.{InterfaceSchemaDB.IFHIGHSPEED.value} AS newIfHighSpeed,
                    newInterface.{InterfaceSchemaDB.IFOPERSTATUS.value} AS newIfOperStatus,
                    newInterface.{InterfaceSchemaDB.IFADMINSTATUS.value} AS newIfAdminStatus,
                    equipment.{EquipmentSchemaDB.IP.value} AS ip,
                    equipment.{EquipmentSchemaDB.COMMUNITY.value} AS community,
                    equipment.{EquipmentSchemaDB.SYSNAME.value} AS sysname,
                    newInterface.{InterfaceSchemaDB.IFINDEX.value} AS ifIndex,
                    o.{OperatorSchemaDB.USERNAME.value} AS username,
                    o.{OperatorSchemaDB.NAME.value} AS name,
                    o.{OperatorSchemaDB.LASTNAME.value} AS lastname
                FROM {GTABLES.ASSIGNMENT.value} a
                JOIN
                    {GTABLES.OPERATOR.value} o ON a.{AssignmentSchemaDB.OPERATOR.value} = o.{OperatorSchemaDB.USERNAME.value}
                JOIN

                JOIN
                    {GTABLES.INTERFACE.value} newInterface ON a.{AssignmentSchemaDB.NEW_INTERFACE.value} = newInterface.{InterfaceSchemaDB.ID.value}
                JOIN
                    {GTABLES.EQUIPMENT.value} equipment ON newInterface.{InterfaceSchemaDB.ID_EQUIPMENT.value} = equipment.{EquipmentSchemaDB.ID.value}
                WHERE
                    a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} <> %s AND
                    EXTRACT(MONTH FROM a.{AssignmentSchemaDB.DATE_ASSIGNMENT.value}) = %s
                """,
                (StatusAssignmentType.PENDING.value, month),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return AssignmentResponse.convert_to_dict_interface_assigned_version(result)
        except Exception as e:
            Log.save(str(e), __file__, Log.error)
            return []

    def get_statistics_assignments_operator(self) -> AssignmentStatisticsOperatorSchema | None:
        """Get the total number of pending and revised assignments of an operator in the database."""
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT
                    o.{OperatorSchemaDB.USERNAME.value} AS username,
                    o.{OperatorSchemaDB.NAME.value} AS name,
                    o.{OperatorSchemaDB.LASTNAME.value} AS lastname,
                    COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_pending_assignments,
                    COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} <> '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_revised_assignments
                FROM {GTABLES.OPERATOR.value} o
                LEFT JOIN
                    {GTABLES.ASSIGNMENT.value} a ON o.{OperatorSchemaDB.USERNAME.value} = a.{AssignmentSchemaDB.OPERATOR.value}
                WHERE
                    a.{AssignmentSchemaDB.OPERATOR.value} = %s
                GROUP BY
                    o.{OperatorSchemaDB.USERNAME.value}
                """,
                (self.operator,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return None
            return AssignmentResponse.convert_to_dict_operator_statistics_version(result)[0]
        except Exception as e:
            Log.save(str(e), __file__, Log.error, console=True)
            return None

    def get_statistics_assingments_operator_by_day(self, day: str) -> AssignmentStatisticsOperatorSchema | None:
        """Get the total number of pending and revised assignments of an operator on the day in the database.

        Parameters
        -----------
        day : str
            Day to get the statistics.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT
                    o.{OperatorSchemaDB.USERNAME.value} AS username,
                    o.{OperatorSchemaDB.NAME.value} AS name,
                    o.{OperatorSchemaDB.LASTNAME.value} AS lastname,
                    COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_pending_assignments,
                    COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} <> '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_revised_assignments
                FROM {GTABLES.OPERATOR.value} o
                LEFT JOIN
                    {GTABLES.ASSIGNMENT.value} a ON o.{OperatorSchemaDB.USERNAME.value} = a.{AssignmentSchemaDB.OPERATOR.value}
                WHERE
                    a.{AssignmentSchemaDB.OPERATOR.value} = %s AND
                    a.{AssignmentSchemaDB.DATE_ASSIGNMENT.value} = %s
                GROUP BY
                    o.{OperatorSchemaDB.USERNAME.value}
                """,
                (self.operator, day),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return None
            return AssignmentResponse.convert_to_dict_operator_statistics_version(result)[0]
        except Exception as e:
            Log.save(str(e), __file__, Log.error, console=True)
            return None

    def get_statistics_assingments_operator_by_month(self, month: int) -> AssignmentStatisticsOperatorSchema | None:
        """Get the total number of pending and revised assignments of an operator on the month in the database.

        Parameters
        -----------
        month : int
            Month to get the statistics.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT
                    o.{OperatorSchemaDB.USERNAME.value} AS username,
                    o.{OperatorSchemaDB.NAME.value} AS name,
                    o.{OperatorSchemaDB.LASTNAME.value} AS lastname,
                    COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_pending_assignments,
                    COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} <> '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_revised_assignments
                FROM {GTABLES.OPERATOR.value} o
                LEFT JOIN
                    {GTABLES.ASSIGNMENT.value} a ON o.{OperatorSchemaDB.USERNAME.value} = a.{AssignmentSchemaDB.OPERATOR.value}
                WHERE
                    a.{AssignmentSchemaDB.OPERATOR.value} = %s AND
                    EXTRACT(MONTH FROM a.{AssignmentSchemaDB.DATE_ASSIGNMENT.value}) = %s
                GROUP BY
                    o.{OperatorSchemaDB.USERNAME.value}
                """,
                (self.operator, month),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return None
            return AssignmentResponse.convert_to_dict_operator_statistics_version(result)[0]
        except Exception as e:
            Log.save(str(e), __file__, Log.error, console=True)
            return None

    def get_all_assignments_by_operator(self) -> List[AssignmentSchema]:
        """Get all assignments of the an operator. \n
        Note: Its necessary declare the username operator in the constructor.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT * FROM {GTABLES.ASSIGNMENT.value}
                WHERE {AssignmentSchemaDB.OPERATOR.value} = %s""",
                (self.operator,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return AssignmentResponse.convert_to_dict(result)
        except Exception as e:
            Log.save(str(e), __file__, Log.error)
            return []

    def get_all_info_assignments_by_operator(self) -> List[AssignmentInterfaceSchema]:
        """Get all interfaces assignments of the an operator. \n
        Note: Its necessary declare the username operator in the constructor.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT
                    a.id AS idAssignment,
                    a.{AssignmentSchemaDB.DATE_ASSIGNMENT.value},
                    a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value},
                    a.{AssignmentSchemaDB.ASSIGNED_BY.value},
                    a.{AssignmentSchemaDB.UPDATED_AT.value},
                    oldInterface.{InterfaceSchemaDB.IFNAME.value} AS oldIfName,
                    oldInterface.{InterfaceSchemaDB.IFDESCR.value} AS oldIfDescr,
                    oldInterface.{InterfaceSchemaDB.IFALIAS.value} AS oldIfAlias,
                    oldInterface.{InterfaceSchemaDB.IFHIGHSPEED.value} AS oldIfHighSpeed,
                    oldInterface.{InterfaceSchemaDB.IFOPERSTATUS.value} AS oldIfOperStatus,
                    oldInterface.{InterfaceSchemaDB.IFADMINSTATUS.value} AS oldIfAdminStatus,
                    newInterface.{InterfaceSchemaDB.IFNAME.value} AS newIfName,
                    newInterface.{InterfaceSchemaDB.IFDESCR.value} AS newIfDescr,
                    newInterface.{InterfaceSchemaDB.IFALIAS.value} AS newIfAlias,
                    newInterface.{InterfaceSchemaDB.IFHIGHSPEED.value} AS newIfHighSpeed,
                    newInterface.{InterfaceSchemaDB.IFOPERSTATUS.value} AS newIfOperStatus,
                    newInterface.{InterfaceSchemaDB.IFADMINSTATUS.value} AS newIfAdminStatus,
                    equipment.{EquipmentSchemaDB.IP.value} AS ip,
                    equipment.{EquipmentSchemaDB.COMMUNITY.value} AS community,
                    equipment.{EquipmentSchemaDB.SYSNAME.value} AS sysname,
                    newInterface.{InterfaceSchemaDB.IFINDEX.value} AS ifIndex
                FROM {GTABLES.ASSIGNMENT.value} a
                JOIN
                    {GTABLES.INTERFACE.value} oldInterface ON a.{AssignmentSchemaDB.OLD_INTERFACE.value} =  oldInterface.{InterfaceSchemaDB.ID.value}
                JOIN
                    {GTABLES.INTERFACE.value} newInterface ON a.{AssignmentSchemaDB.NEW_INTERFACE.value} = newInterface.{InterfaceSchemaDB.ID.value}
                JOIN
                    {GTABLES.EQUIPMENT.value} equipment ON newInterface.{InterfaceSchemaDB.ID_EQUIPMENT.value} = equipment.{EquipmentSchemaDB.ID.value}
                WHERE a.{AssignmentSchemaDB.OPERATOR.value} = %s""",
                (self.operator,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return AssignmentResponse.convert_to_dict_interface_version(result)
        except Exception as e:
            Log.save(str(e), __file__, Log.error)
            return []

    def get_all_info_assignments_pending_by_operator(self) -> List[AssignmentInterfaceSchema]:
        """Get all pending assignments of the an operator. \n
        Note: Its necessary declare the username operator in the constructor.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT
                    a.id AS idAssignment,
                    a.{AssignmentSchemaDB.DATE_ASSIGNMENT.value},
                    a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value},
                    a.{AssignmentSchemaDB.ASSIGNED_BY.value},
                    a.{AssignmentSchemaDB.UPDATED_AT.value},
                    oldInterface.{InterfaceSchemaDB.IFNAME.value} AS oldIfName,
                    oldInterface.{InterfaceSchemaDB.IFDESCR.value} AS oldIfDescr,
                    oldInterface.{InterfaceSchemaDB.IFALIAS.value} AS oldIfAlias,
                    oldInterface.{InterfaceSchemaDB.IFHIGHSPEED.value} AS oldIfHighSpeed,
                    oldInterface.{InterfaceSchemaDB.IFOPERSTATUS.value} AS oldIfOperStatus,
                    oldInterface.{InterfaceSchemaDB.IFADMINSTATUS.value} AS oldIfAdminStatus,
                    newInterface.{InterfaceSchemaDB.IFNAME.value} AS newIfName,
                    newInterface.{InterfaceSchemaDB.IFDESCR.value} AS newIfDescr,
                    newInterface.{InterfaceSchemaDB.IFALIAS.value} AS newIfAlias,
                    newInterface.{InterfaceSchemaDB.IFHIGHSPEED.value} AS newIfHighSpeed,
                    newInterface.{InterfaceSchemaDB.IFOPERSTATUS.value} AS newIfOperStatus,
                    newInterface.{InterfaceSchemaDB.IFADMINSTATUS.value} AS newIfAdminStatus,
                    equipment.{EquipmentSchemaDB.IP.value} AS ip,
                    equipment.{EquipmentSchemaDB.COMMUNITY.value} AS community,
                    equipment.{EquipmentSchemaDB.SYSNAME.value} AS sysname,
                    newInterface.{InterfaceSchemaDB.IFINDEX.value} AS ifIndex
                FROM {GTABLES.ASSIGNMENT.value} a
                JOIN
                    {GTABLES.INTERFACE.value} oldInterface ON a.{AssignmentSchemaDB.OLD_INTERFACE.value} =  oldInterface.{InterfaceSchemaDB.ID.value}
                JOIN
                    {GTABLES.INTERFACE.value} newInterface ON a.{AssignmentSchemaDB.NEW_INTERFACE.value} = newInterface.{InterfaceSchemaDB.ID.value}
                JOIN
                    {GTABLES.EQUIPMENT.value} equipment ON newInterface.{InterfaceSchemaDB.ID_EQUIPMENT.value} = equipment.{EquipmentSchemaDB.ID.value}
                WHERE
                    a.{AssignmentSchemaDB.OPERATOR.value} = %s AND
                    a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = %s
                """,
                (self.operator, StatusAssignmentType.PENDING.value),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return AssignmentResponse.convert_to_dict_interface_version(result)
        except Exception as e:
            Log.save(str(e), __file__, Log.error)
            return []

    def get_all_info_assignments_revised_by_operator(self) -> List[AssignmentInterfaceSchema]:
        """Get all revised assignments of the an operator. \n
        Note: Its necessary declare the username operator in the constructor.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT
                    a.id AS idAssignment,
                    a.{AssignmentSchemaDB.DATE_ASSIGNMENT.value},
                    a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value},
                    a.{AssignmentSchemaDB.ASSIGNED_BY.value},
                    a.{AssignmentSchemaDB.UPDATED_AT.value},
                    oldInterface.{InterfaceSchemaDB.IFNAME.value} AS oldIfName,
                    oldInterface.{InterfaceSchemaDB.IFDESCR.value} AS oldIfDescr,
                    oldInterface.{InterfaceSchemaDB.IFALIAS.value} AS oldIfAlias,
                    oldInterface.{InterfaceSchemaDB.IFHIGHSPEED.value} AS oldIfHighSpeed,
                    oldInterface.{InterfaceSchemaDB.IFOPERSTATUS.value} AS oldIfOperStatus,
                    oldInterface.{InterfaceSchemaDB.IFADMINSTATUS.value} AS oldIfAdminStatus,
                    newInterface.{InterfaceSchemaDB.IFNAME.value} AS newIfName,
                    newInterface.{InterfaceSchemaDB.IFDESCR.value} AS newIfDescr,
                    newInterface.{InterfaceSchemaDB.IFALIAS.value} AS newIfAlias,
                    newInterface.{InterfaceSchemaDB.IFHIGHSPEED.value} AS newIfHighSpeed,
                    newInterface.{InterfaceSchemaDB.IFOPERSTATUS.value} AS newIfOperStatus,
                    newInterface.{InterfaceSchemaDB.IFADMINSTATUS.value} AS newIfAdminStatus,
                    equipment.{EquipmentSchemaDB.IP.value} AS ip,
                    equipment.{EquipmentSchemaDB.COMMUNITY.value} AS community,
                    equipment.{EquipmentSchemaDB.SYSNAME.value} AS sysname,
                    newInterface.{InterfaceSchemaDB.IFINDEX.value} AS ifIndex
                FROM {GTABLES.ASSIGNMENT.value} a
                JOIN
                    {GTABLES.INTERFACE.value} oldInterface ON a.{AssignmentSchemaDB.OLD_INTERFACE.value} =  oldInterface.{InterfaceSchemaDB.ID.value}
                JOIN
                    {GTABLES.INTERFACE.value} newInterface ON a.{AssignmentSchemaDB.NEW_INTERFACE.value} = newInterface.{InterfaceSchemaDB.ID.value}
                JOIN
                    {GTABLES.EQUIPMENT.value} equipment ON newInterface.{InterfaceSchemaDB.ID_EQUIPMENT.value} = equipment.{EquipmentSchemaDB.ID.value}
                WHERE
                    a.{AssignmentSchemaDB.OPERATOR.value} = %s AND
                    a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} <> %s
                """,
                (self.operator, StatusAssignmentType.PENDING.value),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return AssignmentResponse.convert_to_dict_interface_version(result)
        except Exception as e:
            Log.save(str(e), __file__, Log.error)
            return []

    def get_assignment_by_interface(self) -> AssignmentSchema | None:
        """Get an assignment filter by:
        - ID interface (new/change version)
        - ID interface (old version)
        - Username of the operator. \n
        Note: Its necessary declare all information in in the constructor.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT * FROM {GTABLES.ASSIGNMENT.value}
                WHERE {AssignmentSchemaDB.NEW_INTERFACE.value} = %s AND
                {AssignmentSchemaDB.OLD_INTERFACE.value} = %s AND
                {AssignmentSchemaDB.OPERATOR.value} = %s""",
                (self.id_change_interface, self.id_old_interface, self.operator),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            return AssignmentResponse.convert_to_dict([result])[0]
        except Exception as e:
            Log.save(str(e), __file__, Log.error)
            return None

    def get_assignment_by_id_assignment(self) -> AssignmentSchema | None:
        """Get info of the assignment by ID. \n
        Note: Its necessary declare the ID assignment in the constructor.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT * FROM {GTABLES.ASSIGNMENT.value}
                WHERE {AssignmentSchemaDB.ID.value} = %s""",
                (self.id,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            return AssignmentResponse.convert_to_dict([result])[0]
        except Exception as e:
            Log.save(str(e), __file__, Log.error)
            return None

    def get_info_assignment_by_id_assignment(self) -> AssignmentInterfaceSchema | None:
        """Get all information (interfaces, operator, etc.) of the an assignment by ID. \n
        Note: Its necessary declare the ID assignment in the constructor.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT
                    a.id AS idAssignment,
                    a.{AssignmentSchemaDB.DATE_ASSIGNMENT.value},
                    a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value},
                    a.{AssignmentSchemaDB.ASSIGNED_BY.value},
                    a.{AssignmentSchemaDB.UPDATED_AT.value},
                    oldInterface.{InterfaceSchemaDB.IFNAME.value} AS oldIfName,
                    oldInterface.{InterfaceSchemaDB.IFDESCR.value} AS oldIfDescr,
                    oldInterface.{InterfaceSchemaDB.IFALIAS.value} AS oldIfAlias,
                    oldInterface.{InterfaceSchemaDB.IFHIGHSPEED.value} AS oldIfHighSpeed,
                    oldInterface.{InterfaceSchemaDB.IFOPERSTATUS.value} AS oldIfOperStatus,
                    oldInterface.{InterfaceSchemaDB.IFADMINSTATUS.value} AS oldIfAdminStatus,
                    newInterface.{InterfaceSchemaDB.IFNAME.value} AS newIfName,
                    newInterface.{InterfaceSchemaDB.IFDESCR.value} AS newIfDescr,
                    newInterface.{InterfaceSchemaDB.IFALIAS.value} AS newIfAlias,
                    newInterface.{InterfaceSchemaDB.IFHIGHSPEED.value} AS newIfHighSpeed,
                    newInterface.{InterfaceSchemaDB.IFOPERSTATUS.value} AS newIfOperStatus,
                    newInterface.{InterfaceSchemaDB.IFADMINSTATUS.value} AS newIfAdminStatus,
                    equipment.{EquipmentSchemaDB.IP.value} AS ip,
                    equipment.{EquipmentSchemaDB.COMMUNITY.value} AS community,
                    equipment.{EquipmentSchemaDB.SYSNAME.value} AS sysname,
                    newInterface.{InterfaceSchemaDB.IFINDEX.value} AS ifIndex
                FROM {GTABLES.ASSIGNMENT.value} a
                JOIN
                    {GTABLES.INTERFACE.value} oldInterface ON a.{AssignmentSchemaDB.OLD_INTERFACE.value} =  oldInterface.{InterfaceSchemaDB.ID.value}
                JOIN
                    {GTABLES.INTERFACE.value} newInterface ON a.{AssignmentSchemaDB.NEW_INTERFACE.value} = newInterface.{InterfaceSchemaDB.ID.value}
                JOIN
                    {GTABLES.EQUIPMENT.value} equipment ON newInterface.{InterfaceSchemaDB.ID_EQUIPMENT.value} = equipment.{EquipmentSchemaDB.ID.value}
                WHERE a.{AssignmentSchemaDB.ID.value} = %s""",
                (self.id,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            return AssignmentResponse.convert_to_dict_interface_version([result])[0]
        except Exception as e:
            Log.save(str(e), __file__, Log.error)
            return None

    def update_status(self, status: str) -> bool:
        """Update status of the assignment. \n
        Note: Its necessary declare the ID assignment in the constructor.

        Parameters
        ----------
        status : str
            New status of the assignment.
            - **PENDING:** Pending assignment.
            - **INSPECTED:** Inspected assignment.
            - **REDISCOVERED:** Rediscovered assignment.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                UPDATE {GTABLES.ASSIGNMENT.value}
                SET {AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = %s,
                {AssignmentSchemaDB.UPDATED_AT.value} = NOW()
                WHERE {AssignmentSchemaDB.ID.value} = %s""",
                (status.upper(), self.id),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            Log.save(str(e), __file__, Log.error)
            return False
        else:
            if status and status == "UPDATE 1":
                return True
            else:
                return False

    @staticmethod
    def update_status_by_ids(ids: List[int], status: str) -> bool:
        """Update status of many assignments. \n
        Note: Its necessary declare the ID assignment in the constructor.

        Parameters
        ----------
        ids: List[int]
            List of IDs of the assignments.
        status : str
            New status of the assignment.
            - **PENDING:** Pending assignment.
            - **INSPECTED:** Inspected assignment.
            - **REDISCOVERED:** Rediscovered assignment.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            query = sql.SQL("""
                UPDATE
                    {table}
                SET
                    {status_column} = %s,
                    {updated_at_column} = NOW()
                WHERE
                    {id_column} IN ({ids})
            """).format(
                table=sql.Identifier(GTABLES.ASSIGNMENT.value),
                status_column=sql.Identifier(AssignmentSchemaDB.STATUS_ASSIGNMENT.value),
                updated_at_column=sql.Identifier(AssignmentSchemaDB.UPDATED_AT.value),
                id_column=sql.Identifier(AssignmentSchemaDB.ID.value),
                ids=sql.SQL(',').join(map(sql.Literal, ids))
            )
            cursor.execute(query, (status.upper(),))
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            Log.save(str(e), __file__, Log.error, console=True)
            return False
        else:
            if status and "UPDATE" in status:
                return True
            else:
                return False

    def delete(self) -> bool:
        """Delete the assignment with the given ID. \n
        Note: Its necessary declare the ID assignment in the constructor.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                DELETE FROM {GTABLES.ASSIGNMENT.value}
                WHERE {AssignmentSchemaDB.ID.value} = %s""",
                (self.id,),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            Log.save(str(e), __file__, Log.error)
            return False
        else:
            if status and status == "DELETE 1":
                return True
            else:
                return False
