from typing import List
from psycopg2 import sql
from constants import StatusAssignmentType
from database import PostgresDatabase, GTABLES, AssignmentSchemaDB, InterfaceSchemaDB, EquipmentSchemaDB, OperatorSchemaDB
from schemas import AssignmentResponseSchema, AssignmentInterfaceResponseSchema, AssignmentStatisticsResponse
from utils import assignment_to_dict, assignment_interface_to_dict, assignment_statistics_to_dict, Log


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
    def get_all_statistics_assingments() -> List[AssignmentStatisticsResponse]:
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
            return assignment_statistics_to_dict(result)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    @staticmethod
    def update_status_by_ids(ids: List[int], status: str) -> bool:
        """Update status of many assignments. \n
        _Note:_ Its necessary declare the ID assignment in the constructor.

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
            Log.save(e, __file__, Log.error, console=True)
            return False
        else:
            if status and "UPDATE" in status:
                return True
            else:
                return False
        
    def get_all_statistics_assingments_by_operator(self) -> AssignmentStatisticsResponse | None:
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
            statistics = assignment_statistics_to_dict(result)
            return statistics[0]
        except Exception as e:
            Log.save(e, __file__, Log.error, console=True)
            return None

    def get_all_assignments_by_operator(self) -> List[AssignmentResponseSchema]:
        """Get all assignments of the an operator. \n
        _Note:_ Its necessary declare the username operator in the constructor.
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
            return assignment_to_dict(result)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    def get_all_info_assignments_by_operator(self) -> List[AssignmentInterfaceResponseSchema]:
        """Get all interfaces assignments of the an operator. \n
        _Note:_ Its necessary declare the username operator in the constructor.
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
                    {GTABLES.INTERFACE.value} newInterface ON a.{AssignmentSchemaDB.CHANGE_INTERFACE.value} = newInterface.{InterfaceSchemaDB.ID.value}
                JOIN
                    {GTABLES.EQUIPMENT.value} equipment ON newInterface.{InterfaceSchemaDB.ID_EQUIPMENT.value} = equipment.{EquipmentSchemaDB.ID.value}
                WHERE a.{AssignmentSchemaDB.OPERATOR.value} = %s""",
                (self.operator,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return assignment_interface_to_dict(result)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    def get_assignment_by_interface(self) -> AssignmentResponseSchema | None:
        """Get an assignment filter by:
        - ID interface (new/change version)
        - ID interface (old version)
        - Username of the operator. \n
        _Note:_ Its necessary declare all information in in the constructor.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT * FROM {GTABLES.ASSIGNMENT.value}
                WHERE {AssignmentSchemaDB.CHANGE_INTERFACE.value} = %s AND
                {AssignmentSchemaDB.OLD_INTERFACE.value} = %s AND
                {AssignmentSchemaDB.OPERATOR.value} = %s""",
                (self.id_change_interface, self.id_old_interface, self.operator),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            assignment = assignment_to_dict([result])
            return assignment[0]
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    def get_by_id_assignment(self) -> AssignmentResponseSchema | None:
        """Get info of the assignment by ID. \n
        _Note:_ Its necessary declare the ID assignment in the constructor.
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
            assignment = assignment_to_dict([result])
            return assignment[0]
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    def get_info_assignment_by_id(self) -> AssignmentInterfaceResponseSchema | None:
        """Get all information (interfaces, operator, etc.) of the an assignment by ID. \n
        _Note:_ Its necessary declare the ID assignment in the constructor.
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
                    {GTABLES.INTERFACE.value} newInterface ON a.{AssignmentSchemaDB.CHANGE_INTERFACE.value} = newInterface.{InterfaceSchemaDB.ID.value}
                JOIN
                    {GTABLES.EQUIPMENT.value} equipment ON newInterface.{InterfaceSchemaDB.ID_EQUIPMENT.value} = equipment.{EquipmentSchemaDB.ID.value}
                WHERE a.{AssignmentSchemaDB.ID.value} = %s""",
                (self.id,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            assignment = assignment_interface_to_dict([result])
            return assignment[0]
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    def update_operator(self, username: str, assigned_by: str) -> bool:
        """Reassing the assignment to another operator. \n
        _Note:_ Its necessary declare the ID assignment in the constructor.

        Parameters
        ----------
        username : str
            Username of the new operator.
        assigned_by : str
            Username of the operator who assigned the assignment.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                UPDATE {GTABLES.ASSIGNMENT.value}
                SET {AssignmentSchemaDB.OPERATOR.value} = %s,
                {AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = %s,
                {AssignmentSchemaDB.ASSIGNED_BY.value} = %s,
                {AssignmentSchemaDB.UPDATED_AT.value} = NOW()
                WHERE {AssignmentSchemaDB.ID.value} = %s""",
                (username, StatusAssignmentType.PENDING.value, assigned_by.upper(), self.id),
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

    def update_status(self, status: str) -> bool:
        """Update status of the assignment. \n
        _Note:_ Its necessary declare the ID assignment in the constructor.

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
            Log.save(e, __file__, Log.error)
            return False
        else:
            if status and status == "UPDATE 1":
                return True
            else:
                return False

    def delete(self) -> bool:
        """Delete the assignment with the given ID. \n
        _Note:_ Its necessary declare the ID assignment in the constructor.
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
            Log.save(e, __file__, Log.error)
            return False
        else:
            if status and status == "DELETE 1":
                return True
            else:
                return False
