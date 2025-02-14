from typing import List
from constants import StatusAssignmentType
from database import PostgresDatabase, GTABLES, AssignmentSchemaDB
from schemas import AssignmentSchema
from utils import assignment_to_dict, Log


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
        if operator: self.operator = operator.lower()
        else: self.operator = operator
        self.id_change_interface = id_change_interface
        self.id_old_interface = id_old_interface

    @staticmethod
    def get_count_all_pending() -> int:
        """Get the total number of pending assignments of the system."""
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT COUNT(*) AS total_assignments_pending
                FROM {GTABLES.ASSIGNMENT.value} 
                WHERE {AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = %s""",
                (StatusAssignmentType.PENDING.value,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return 0
            return result[0]
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return 0
        
    @staticmethod
    def get_count_all_revised() -> int:
        """Get the total number of revised assignments of the system."""
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT COUNT(*) AS total_assignments_revised
                FROM {GTABLES.ASSIGNMENT.value} 
                WHERE {AssignmentSchemaDB.STATUS_ASSIGNMENT.value} != %s""",
                (StatusAssignmentType.PENDING.value,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return 0
            return result[0]
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return 0

    @staticmethod 
    def get_all_by_status(status: str) -> List[AssignmentSchema]:
        """Get all assignments filter by an status assignment in the system.

        Parameters
        ----------
        status : str
            Status type of the assignment.
            - **PENDING:** Pending assignment.
            - **INSPECTED:** Inspected assignment.
            - **REDISCOVERED:** Rediscovered assignment.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT * FROM {GTABLES.ASSIGNMENT.value} 
                WHERE {AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = %s""",
                (status.upper(),),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return assignment_to_dict(result)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []
        
    def get_count_pending_by_operator(self) -> int:
        """Get the total number of pending assignments of the an operator. \n
        _Note:_ Its necessary declare the username operator in the constructor.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT COUNT(*) AS total_assignments_pending
                FROM {GTABLES.ASSIGNMENT.value} 
                WHERE {AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = %s AND
                WHERE {AssignmentSchemaDB.OPERATOR.value} = %s""",
                (StatusAssignmentType.PENDING.value, self.operator),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return 0
            return result[0]
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return 0
        
    def get_count_revised_by_operator(self) -> int:
        """Get the total number of revised assignments of the an operator. \n
        _Note:_ Its necessary declare the username operator in the constructor.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT COUNT(*) AS total_assignments_pending
                FROM {GTABLES.ASSIGNMENT.value} 
                WHERE {AssignmentSchemaDB.STATUS_ASSIGNMENT.value} != %s AND
                WHERE {AssignmentSchemaDB.OPERATOR.value} = %s""",
                (StatusAssignmentType.PENDING.value, self.operator),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return 0
            return result[0]
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return 0

    def get_all_status_by_operator(self, status: str) -> List[AssignmentSchema]:
        """Get all assignments filter by an status assignment of the an operator. \n
        _Note:_ Its necessary declare the username operator in the constructor.

        Parameters
        ----------
        status : str
            Status type of the assignment.
            - **PENDING:** Pending assignment.
            - **INSPECTED:** Inspected assignment.
            - **REDISCOVERED:** Rediscovered assignment.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                SELECT * FROM {GTABLES.ASSIGNMENT.value} 
                WHERE {AssignmentSchemaDB.STATUS_ASSIGNMENT.value} = %s AND
                {AssignmentSchemaDB.OPERATOR.value} = %s""",
                (status.upper(), self.operator),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return assignment_to_dict(result)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    def get_all_by_operator(self) -> List[AssignmentSchema]:
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

    def get_assignment_by_interface(self) -> AssignmentSchema | None:
        """Get all assignments filter by: 
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

    def get_by_id(self) -> AssignmentSchema | None:
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
