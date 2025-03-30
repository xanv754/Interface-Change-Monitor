from typing import List
from psycopg2 import sql
from constants.types import StatusAssignmentType
from database.constants.tables import Tables as GTABLES # Global Tables
from database.database import PostgresDatabase
from database.schemas.assignment import AssignmentSchemaDB
from database.schemas.interface import InterfaceSchemaDB
from database.schemas.equipment import EquipmentSchemaDB
from database.schemas.operator import OperatorSchemaDB
from schemas.assignment import (
    RegisterAssignmentBody,
    ReassignBody,
    AssignmentSchema,
    AssignmentInterfaceSchema,
    AssignmentInterfaceAssignedSchema,
    AssignmentStatisticsSchema,
    AssignmentStatisticsOperatorSchema
)
from utils.log import LogHandler
from utils.convert import AssignmentResponse


class AssignmentModel:
    """Model for all queries of the assignments table."""

    @staticmethod
    def register(assignments: List[RegisterAssignmentBody]) -> bool:
        """Register an new assignment in the database.

        Parameters
        ----------
        assingments : RegisterAssignmentBody
            List of new assignments to register.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            with cursor:
                query = sql.SQL(
                    """
                        INSERT INTO {table} (
                            {change_interface},
                            {old_interface},
                            {operator},
                            {date_assignment},
                            {status_assignment},
                            {assigned_by}
                        )
                        VALUES (%s, %s, %s, CURRENT_DATE, %s, %s)
                    """
                ).format(
                        table=sql.Identifier(GTABLES.ASSIGNMENT.value),
                        change_interface=sql.Identifier(AssignmentSchemaDB.NEW_INTERFACE.value),
                        old_interface=sql.Identifier(AssignmentSchemaDB.OLD_INTERFACE.value),
                        operator=sql.Identifier(AssignmentSchemaDB.OPERATOR.value),
                        date_assignment=sql.Identifier(AssignmentSchemaDB.DATE_ASSIGNMENT.value),
                        status_assignment=sql.Identifier(AssignmentSchemaDB.STATUS_ASSIGNMENT.value),
                        assigned_by=sql.Identifier(AssignmentSchemaDB.ASSIGNED_BY.value)
                    )
                for assignment in assignments:
                    cursor.execute(query, (
                        assignment.newInterface,
                        assignment.oldInterface,
                        assignment.operator,
                        StatusAssignmentType.PENDING.value,
                        assignment.assignedBy
                    ))
            connection.commit()
            response_status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if response_status and "INSERT" in response_status:
                return True
            else:
                return False

    @staticmethod
    def reassing(assignments: List[ReassignBody]) -> bool:
        """Reassign an assignment for an operator.

        Parameters
        ----------
        assingments : RegisterAssignmentBody
            List of assignments to reassign an operator.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            with cursor:
                query = sql.SQL(
                    """
                        UPDATE
                            {table}
                        SET
                            {operator} = %s,
                            {assigned_by} = %s,
                            {status_assignment} = %s
                        WHERE
                            {id} = %s
                    """
                ).format(
                        table=sql.Identifier(GTABLES.ASSIGNMENT.value),
                        operator=sql.Identifier(AssignmentSchemaDB.OPERATOR.value),
                        assigned_by=sql.Identifier(AssignmentSchemaDB.ASSIGNED_BY.value),
                        status_assignment=sql.Identifier(AssignmentSchemaDB.STATUS_ASSIGNMENT.value),
                        id=sql.Identifier(AssignmentSchemaDB.ID.value)
                    )
                for assignment in assignments:
                    cursor.execute(query, (
                        assignment.newOperator,
                        assignment.assignedBy,
                        StatusAssignmentType.PENDING.value,
                        assignment.idAssignment
                    ))
            connection.commit()
            response_status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if response_status and "UPDATE" in response_status:
                return True
            else:
                return False

    @staticmethod
    def get_by_id(id: int) -> AssignmentSchema | None:
        """Get info of the assignment by ID. \n

        Parameters
        ----------
        id : int
            Assignment's ID.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT *
                    FROM
                        {GTABLES.ASSIGNMENT.value}
                    WHERE
                        {AssignmentSchemaDB.ID.value} = %s
                """,
                (id,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            return AssignmentResponse.convert_to_dict([result])[0]
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_by_operator(username: str) -> List[AssignmentSchema]:
        """Get all assignments of the an operator.

        Parameters
        ----------
        username : str
            Operator's username.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT *
                    FROM
                        {GTABLES.ASSIGNMENT.value}
                    WHERE
                        {AssignmentSchemaDB.OPERATOR.value} = %s
                """,
                (username,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return AssignmentResponse.convert_to_dict(result)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_by_interfaces(id_new_interface: int, id_old_interface: int, username: str) -> AssignmentSchema | None:
        """Get an assignment filter by:
            - ID interface (new version)
            - ID interface (old version)
            - Username of the operator.

        Parameters
        ----------
        id_new_interface : int
            ID new interface.
        id_old_interface : int
            ID old interface.
        username : str
            Operator's username.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT *
                    FROM
                        {GTABLES.ASSIGNMENT.value}
                    WHERE
                        {AssignmentSchemaDB.NEW_INTERFACE.value} = %s AND
                        {AssignmentSchemaDB.OLD_INTERFACE.value} = %s AND
                        {AssignmentSchemaDB.OPERATOR.value} = %s
                """,
                (id_new_interface, id_old_interface, username),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            return AssignmentResponse.convert_to_dict([result])[0]
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def update_status_by_id(id: int, status: str) -> bool:
        """Update status of the assignment by an ID.

        Parameters
        ----------
        id : int
            Assignment's ID.
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
                    UPDATE
                        {GTABLES.ASSIGNMENT.value}
                    SET
                        {AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = %s,
                        {AssignmentSchemaDB.UPDATED_AT.value} = NOW()
                    WHERE
                        {AssignmentSchemaDB.ID.value} = %s
                """,
                (status.upper(), id),
            )
            connection.commit()
            response_status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if response_status and response_status == "UPDATE 1":
                return True
            else:
                return False

    @staticmethod
    def update_status(ids: List[int], status: str) -> bool:
        """Update status of many assignments.

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
            query = sql.SQL(
                """
                    UPDATE
                        {table}
                    SET
                        {status_column} = %s,
                        {updated_at_column} = NOW()
                    WHERE
                        {id_column} IN ({ids})
                """
            ).format(
                table=sql.Identifier(GTABLES.ASSIGNMENT.value),
                status_column=sql.Identifier(AssignmentSchemaDB.STATUS_ASSIGNMENT.value),
                updated_at_column=sql.Identifier(AssignmentSchemaDB.UPDATED_AT.value),
                id_column=sql.Identifier(AssignmentSchemaDB.ID.value),
                ids=sql.SQL(',').join(map(sql.Literal, ids))
            )
            cursor.execute(query, (status.upper(),))
            connection.commit()
            response_status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if response_status and "UPDATE" in response_status:
                return True
            else:
                return False

    @staticmethod
    def delete(id: int) -> bool:
        """Delete the assignment by an ID.

        Parameters
        ----------
        id : int
            Assignment's ID.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    DELETE FROM
                        {GTABLES.ASSIGNMENT.value}
                    WHERE
                        {AssignmentSchemaDB.ID.value} = %s
                """,
                (id,),
            )
            connection.commit()
            response_status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if response_status and response_status == "DELETE 1":
                return True
            else:
                return False


class AssignmentStatisticsModel:
    """Model for all queries to generate statistics."""

    @staticmethod
    def get_general_by_day(day: str) -> AssignmentStatisticsSchema | None:
        """Get the total number of pending and revised assignments in general by a day.

        Parameters
        ----------
        day : str
            Day to consult.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT
                        COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_pending_assignments,
                        COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} <> '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_revised_assignments
                    FROM
                        {GTABLES.ASSIGNMENT.value} a
                    WHERE
                        a.{AssignmentSchemaDB.DATE_ASSIGNMENT.value} = %s
                """,
                (day,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            return AssignmentResponse.convert_to_dict_statistics_version(result)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_general_by_month(month: int) -> AssignmentStatisticsSchema | None:
        """Get the total number of pending and revised assignments in general by a month.

        Parameters
        ----------
        month : int
            Month to consult.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT
                        COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_pending_assignments,
                        COUNT(CASE WHEN a.{AssignmentSchemaDB.STATUS_ASSIGNMENT.value} <> '{StatusAssignmentType.PENDING.value}' THEN 1 END) AS total_revised_assignments
                    FROM
                        {GTABLES.ASSIGNMENT.value} a
                    WHERE
                        EXTRACT(MONTH FROM a.{AssignmentSchemaDB.DATE_ASSIGNMENT.value}) = %s
                """,
                (month,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            return AssignmentResponse.convert_to_dict_statistics_version(result)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_general_by_operators() -> List[AssignmentStatisticsOperatorSchema]:
        """Get the total number of pending and revised assignments of all operators."""
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
                    FROM
                        {GTABLES.OPERATOR.value} o
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
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_general_operators_by_day(day: str) -> List[AssignmentStatisticsOperatorSchema]:
        """Get the total number of pending and revised assignments of all operators by a day.

        Parameters
        -----------
        day : str
            Day to consult.
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
                    FROM
                        {GTABLES.OPERATOR.value} o
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
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_general_operators_by_month(month: int) -> List[AssignmentStatisticsOperatorSchema]:
        """Get the total number of pending and revised assignments of all operators by a month.

        Parameters
        -----------
        month : int
            Month to consult.
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
                    FROM
                        {GTABLES.OPERATOR.value} o
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
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_operator(username: str) -> AssignmentStatisticsOperatorSchema | None:
        """Get the total number of pending and revised assignments of an operator.

        Parameters
        ----------
        username : str
            Operator's username.
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
                    FROM
                        {GTABLES.OPERATOR.value} o
                    LEFT JOIN
                        {GTABLES.ASSIGNMENT.value} a ON o.{OperatorSchemaDB.USERNAME.value} = a.{AssignmentSchemaDB.OPERATOR.value}
                    WHERE
                        a.{AssignmentSchemaDB.OPERATOR.value} = %s
                """,
                (username,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return None
            return AssignmentResponse.convert_to_dict_operator_statistics_version(result)[0]
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_operator_by_month(username: str, month: int) -> AssignmentStatisticsOperatorSchema | None:
        """Get the total number of pending and revised assignments of an operator by a month.

        Parameters
        -----------
        username : str
            Operator's username.
        month : int
            Month to consult.
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
                    FROM
                        {GTABLES.OPERATOR.value} o
                    LEFT JOIN
                        {GTABLES.ASSIGNMENT.value} a ON o.{OperatorSchemaDB.USERNAME.value} = a.{AssignmentSchemaDB.OPERATOR.value}
                    WHERE
                        a.{AssignmentSchemaDB.OPERATOR.value} = %s AND
                        EXTRACT(MONTH FROM a.{AssignmentSchemaDB.DATE_ASSIGNMENT.value}) = %s
                """,
                (username, month),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return None
            return AssignmentResponse.convert_to_dict_operator_statistics_version(result)[0]
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_operator_by_day(username: str, day: str) -> AssignmentStatisticsOperatorSchema | None:
        """Get the total number of pending and revised assignments of an operator by a day.

        Parameters
        -----------
        username : str
            Operator's username.
        day : str
            Day to consult.
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
                    FROM
                        {GTABLES.OPERATOR.value} o
                    LEFT JOIN
                        {GTABLES.ASSIGNMENT.value} a ON o.{OperatorSchemaDB.USERNAME.value} = a.{AssignmentSchemaDB.OPERATOR.value}
                    WHERE
                        a.{AssignmentSchemaDB.OPERATOR.value} = %s AND
                        a.{AssignmentSchemaDB.DATE_ASSIGNMENT.value} = %s
                """,
                (username, day),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return None
            return AssignmentResponse.convert_to_dict_operator_statistics_version(result)[0]
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

class AssignmentInfoModel:
    """Model for all queries obtaining all the information of the assignments with their interfaces."""

    @staticmethod
    def get_by_id(id: int) -> AssignmentInterfaceSchema | None:
        """Get all information of the an assignment by ID.

        Parameters
        ----------
        id : int
            Assignment's ID.
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
                    FROM
                        {GTABLES.ASSIGNMENT.value} a
                    JOIN
                        {GTABLES.INTERFACE.value} oldInterface ON a.{AssignmentSchemaDB.OLD_INTERFACE.value} =  oldInterface.{InterfaceSchemaDB.ID.value}
                    JOIN
                        {GTABLES.INTERFACE.value} newInterface ON a.{AssignmentSchemaDB.NEW_INTERFACE.value} = newInterface.{InterfaceSchemaDB.ID.value}
                    JOIN
                        {GTABLES.EQUIPMENT.value} equipment ON newInterface.{InterfaceSchemaDB.ID_EQUIPMENT.value} = equipment.{EquipmentSchemaDB.ID.value}
                    WHERE
                        a.{AssignmentSchemaDB.ID.value} = %s
                """,
                (id,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            return AssignmentResponse.convert_to_dict_interface_version([result])[0]
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_by_operator(username: str) -> List[AssignmentInterfaceSchema]:
        """Get assignments with all information of the an operator.

        Parameters
        ----------
        username : str
            Operator's username.
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
                        a.{AssignmentSchemaDB.OPERATOR.value} = %s
                """,
                (username,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return AssignmentResponse.convert_to_dict_interface_version(result)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_revised_by_month(month: int) -> List[AssignmentInterfaceAssignedSchema]:
        """Get all revised assignments of all operators by a month.

        Parameters
        ----------
        month : int
            Month to consult.
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
                    FROM
                        {GTABLES.ASSIGNMENT.value} a
                    JOIN
                        {GTABLES.OPERATOR.value} o ON a.{AssignmentSchemaDB.OPERATOR.value} = o.{OperatorSchemaDB.USERNAME.value}
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
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_pending(username: str) -> List[AssignmentInterfaceSchema]:
        """Get all pending assignments of the an operator.

        Parameters
        -----------
        username : str
            Operator's username.
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
                    FROM
                        {GTABLES.ASSIGNMENT.value} a
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
                (username, StatusAssignmentType.PENDING.value),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return AssignmentResponse.convert_to_dict_interface_version(result)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_revised(username: str) -> List[AssignmentInterfaceSchema]:
        """Get all revised assignments of the an operator.

        Parameters
        ----------
        username : str
            Operator's username.
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
                    FROM
                        {GTABLES.ASSIGNMENT.value} a
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
                (username, StatusAssignmentType.PENDING.value),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return AssignmentResponse.convert_to_dict_interface_version(result)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []
