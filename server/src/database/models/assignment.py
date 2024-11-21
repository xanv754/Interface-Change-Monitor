from typing import List
from database.entities.assignment import AssignmentEntity
from database.utils.database import Database
from database.constants.assignment import TypeStatusAssignment

class AssignmentModel:
    @staticmethod
    def get_assignment(change_interface: int, old_interface: int, operator: str) -> AssignmentEntity | None:
        """Obtain an assignment by performing a database query.
        
        Parameters
        ----------
        change_interface : int
            The id of the interface with changes.
        old_interface : int
            The id of the old interface.
        operator : str
            The username of the operator.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM assignment WHERE changeInterface = %s AND oldInterface = %s AND operator = %s", (change_interface, old_interface, operator))
        res = cur.fetchone()
        database.close_connection()
        if res:
            data = dict(zip(AssignmentEntity.model_fields.keys(), res))
            assignment = AssignmentEntity(**data)
            return assignment
        else:
            return None
    
    @staticmethod
    def get_assignments() -> List[AssignmentEntity]:
        """Obtain a list of all assignments by performing a database query."""
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM assignment")
        res = cur.fetchall()
        database.close_connection()
        if res:
            assignments: List[AssignmentEntity] = []
            for data in res:
                data = dict(zip(AssignmentEntity.model_fields.keys(), data))
                assignment = AssignmentEntity(**data)
                assignments.append(assignment)
            return assignments
        else:
            return []
        
    @staticmethod
    def get_assignments_by_operator(operator: str) -> List[AssignmentEntity]:
        """Obtain a list of all assignments filter by operator by performing a database query.
        
        Parameters
        ----------
        operator : str
            The username of the operator.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM assignment WHERE operator = %s", (operator,))
        res = cur.fetchall()
        database.close_connection()
        if res:
            assignments: List[AssignmentEntity] = []
            for data in res:
                data = dict(zip(AssignmentEntity.model_fields.keys(), data))
                assignment = AssignmentEntity(**data)
                assignments.append(assignment)
            return assignments
        else:
            return []
        
    @staticmethod
    def get_assignments_by_date_assignment(date_assignment: str) -> List[AssignmentEntity]:
        """Obtain a list of all assignments filter by date assignment by performing a database query.
        
        Parameters
        ----------
        date_assignment : str
            The date of the assignment in format YYYY-MM-DD.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM assignment WHERE dateAssignment = %s", (date_assignment,))
        res = cur.fetchall()
        database.close_connection()
        if res:
            assignments: List[AssignmentEntity] = []
            for data in res:
                data = dict(zip(AssignmentEntity.model_fields.keys(), data))
                assignment = AssignmentEntity(**data)
                assignments.append(assignment)
            return assignments
        else:
            return []
        
    @staticmethod
    def get_assignments_by_status(status: TypeStatusAssignment) -> List[AssignmentEntity]:
        """Obtain a list of all assignments filter by status assignment by performing a database query.
        
        Parameters
        ----------
        status : TypeStatusAssignment
            The status of the assignment.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM assignment WHERE statusAssignment = %s", (status,))
        res = cur.fetchall()
        database.close_connection()
        if res:
            assignments: List[AssignmentEntity] = []
            for data in res:
                data = dict(zip(AssignmentEntity.model_fields.keys(), data))
                assignment = AssignmentEntity(**data)
                assignments.append(assignment)
            return assignments
        else:
            return []
        
    @staticmethod
    def get_assignments_by_assigned(assigned_by: str) -> List[AssignmentEntity]:
        """Obtain a list of all assignments filter by assigned by performing a database query.
        
        Parameters
        ----------
        assigned_by : str
            The username of the operator.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM assignment WHERE assignedBy = %s", (assigned_by,))
        res = cur.fetchall()
        database.close_connection()
        if res:
            assignments: List[AssignmentEntity] = []
            for data in res:
                data = dict(zip(AssignmentEntity.model_fields.keys(), data))
                assignment = AssignmentEntity(**data)
                assignments.append(assignment)
            return assignments
        else:
            return []
        
    @staticmethod
    def get_assignments_by_review(date_review: str) -> List[AssignmentEntity]:
        """Obtain a list of all assignments filter date review by performing a database query.
        
        Parameters
        ----------
        date_review : datetime
            The date of the review in format YYYY-MM-DD.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM assignment WHERE dateReview = %s", (date_review,))
        res = cur.fetchall()
        database.close_connection()
        if res:
            assignments: List[AssignmentEntity] = []
            for data in res:
                data = dict(zip(AssignmentEntity.model_fields.keys(), data))
                assignment = AssignmentEntity(**data)
                assignments.append(assignment)
            return assignments
        else:
            return []
        
