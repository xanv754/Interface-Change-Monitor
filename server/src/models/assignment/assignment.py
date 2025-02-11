from typing import List
from constants import GTABLES, StatusAssignmentType
from database import PostgresDatabase
from schemas import AssignmentSchema
from utils import assignment_to_dict


class Assignment:
    id: int
    username: str

    def __init__(self, id: int | None = None, username: str | None = None):
        self.id = id
        self.username = username

    def get_all_by_operator(self) -> List[dict]:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT * FROM {GTABLES.ASSIGNMENT.value} 
                WHERE {AssignmentSchema.OPERATOR.value} = %s""",
                (self.username,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return assignment_to_dict(result)
        except Exception as e:
            print(e)
            return []

    def get_all_by_status(self, status: str) -> List[dict]:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT * FROM {GTABLES.ASSIGNMENT.value} 
                WHERE {AssignmentSchema.STATUS_ASSIGNMENT.value} = %s AND
                {AssignmentSchema.OPERATOR.value} = %s""",
                (status, self.username),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return assignment_to_dict(result)
        except Exception as e:
            print(e)
            return []

    def update_operator(self, username: str, assigned_by: str) -> bool:
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                UPDATE {GTABLES.ASSIGNMENT.value} 
                SET {AssignmentSchema.OPERATOR.value} = %s,
                {AssignmentSchema.STATUS_ASSIGNMENT.value} = %s,
                {AssignmentSchema.ASSIGNED_BY.value} = %s,
                {AssignmentSchema.UPDATED_AT.value} = NOW()
                WHERE {AssignmentSchema.ID.value} = %s""",
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
                SET {AssignmentSchema.STATUS_ASSIGNMENT.value} = %s,
                {AssignmentSchema.UPDATED_AT.value} = NOW()
                WHERE {AssignmentSchema.ID.value} = %s""",
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
                WHERE {AssignmentSchema.ID.value} = %s""",
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
