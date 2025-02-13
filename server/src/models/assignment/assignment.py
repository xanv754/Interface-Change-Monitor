from typing import List
from constants import StatusAssignmentType
from database import PostgresDatabase, GTABLES, AssignmentSchemaDB
from schemas import AssignmentSchema
from utils import assignment_to_dict


class Assignment:
    id: int
    id_change_interface: int
    id_old_interface: int
    operator: str

    def __init__(
        self,
        id: int | None = None,
        id_change_interface: int | None = None,
        id_old_interface: int | None = None,
        operator: str | None = None,
    ):
        self.id = id
        self.operator = operator
        self.id_change_interface = id_change_interface
        self.id_old_interface = id_old_interface

    def get_all_by_operator(self) -> List[AssignmentSchema]:
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
            print(e)
            return []

    def get_all_by_status(self, status: str) -> List[AssignmentSchema]:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT * FROM {GTABLES.ASSIGNMENT.value} 
                WHERE {AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = %s AND
                {AssignmentSchemaDB.OPERATOR.value} = %s""",
                (status, self.operator),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return assignment_to_dict(result)
        except Exception as e:
            print(e)
            return []

    def get_assignment_by_interface(self) -> AssignmentSchema | None:
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
            print(e)
            return None

    def get_by_id(self) -> AssignmentSchema | None:
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
            print(e)
            return None

    def update_operator(self, username: str, assigned_by: str) -> bool:
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
                (username, StatusAssignmentType.PENDING.value, assigned_by, self.id),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            print(e)
            return False
        else:
            if status and status == "UPDATE 1":
                return True
            else:
                return False

    def update_status(self, status: str) -> bool:
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
                (status, self.id),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            print(e)
            return False
        else:
            if status and status == "UPDATE 1":
                return True
            else:
                return False

    def delete(self) -> bool:
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
            print(e)
            return False
        else:
            if status and status == "DELETE 1":
                return True
            else:
                return False
