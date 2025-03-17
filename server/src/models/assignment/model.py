from psycopg2 import sql
from constants import StatusAssignmentType
from database import PostgresDatabase, GTABLES, AssignmentSchemaDB
from schemas import RegisterAssignmentBody, ReassignBody
from utils import Log

class AssignmentModel:

    def register(self, assignments: list[RegisterAssignmentBody]) -> bool:
        """Register an new assignment in the database. \n
        _Note:_ All the data required by the new assignment is extracted from the constructor.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            with cursor:
                query = sql.SQL("""
                    INSERT INTO {table} ({change_interface}, {old_interface}, {operator}, {date_assignment}, {status_assignment}, {assigned_by})
                    VALUES (%s, %s, %s, CURRENT_DATE, %s, %s)
                """).format(
                        table=sql.Identifier(GTABLES.ASSIGNMENT.value),
                        change_interface=sql.Identifier(AssignmentSchemaDB.CHANGE_INTERFACE.value),
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
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False
        else:
            if status and "INSERT" in status:
                return True
            else:
                return False
            
    def reassing(self, assignments: list[ReassignBody]) -> bool:
        """Reassign an assignment in the database. \n
        _Note:_ All the data required by the new assignment is extracted from the constructor.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            with cursor:
                query = sql.SQL("""
                    UPDATE {table}
                    SET {operator} = %s, {assigned_by} = %s, {status_assignment} = %s
                    WHERE {id} = %s
                """).format(
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
