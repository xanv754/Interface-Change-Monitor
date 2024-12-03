from typing import List
from datetime import datetime
from database.entities.assignment import AssignmentEntity, AssignmentField
from database.utils.database import Database
from database.constants.types.assignment import Status
from database.constants.tables import TableDatabase

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
        cur.execute(f"SELECT * FROM {TableDatabase.assignment.value} WHERE {AssignmentField.changeInterface.value} = %s AND {AssignmentField.oldInterface.value} = %s AND {AssignmentField.operator.value} = %s", (change_interface, old_interface, operator))
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
        cur.execute(f"SELECT * FROM {TableDatabase.assignment.value}")
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
        cur.execute(f"SELECT * FROM {TableDatabase.assignment.value} WHERE {AssignmentField.operator.value} = %s", (operator,))
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
        
    def get_assignments_by_operator_and_status(operator: str, status: Status) -> List[AssignmentEntity]:
        """Obtain a list of all assignments filter by operator and status assignment by performing a database query.
        
        Parameters
        ----------
        operator : str
            The username of the operator.
        status : Status
            The status of the assignment.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute(f"SELECT * FROM {TableDatabase.assignment.value} WHERE {AssignmentField.operator.value} = %s AND {AssignmentField.statusAssignment.value} = %s", (operator, status.value))
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
        cur.execute(f"SELECT * FROM {TableDatabase.assignment.value} WHERE {AssignmentField.dateAssignment.value} = %s", (date_assignment,))
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
    def get_assignments_by_status(status: Status) -> List[AssignmentEntity]:
        """Obtain a list of all assignments filter by status assignment by performing a database query.
        
        Parameters
        ----------
        status : Status
            The status of the assignment.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute(f"SELECT * FROM {TableDatabase.assignment.value} WHERE {AssignmentField.statusAssignment.value} = %s", (status,))
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
        cur.execute(f"SELECT * FROM {TableDatabase.assignment.value} WHERE {AssignmentField.assignedBy.value} = %s", (assigned_by,))
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
        cur.execute(f"SELECT * FROM {TableDatabase.assignment.value} WHERE {AssignmentField.dateReview.value} = %s", (date_review,))
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
    def insert_assignment(data: dict) -> AssignmentEntity | None:
        """Create an assignment by performing a database query.
        
        Parameters
        ----------
        data: dict
            Dict with the values of the assignment to be created.
        """
        new_assignment = AssignmentEntity(**data)
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(f"INSERT INTO {TableDatabase.assignment.value} ({AssignmentField.changeInterface.value}, {AssignmentField.oldInterface.value}, {AssignmentField.operator.value}, {AssignmentField.dateAssignment.value}, {AssignmentField.statusAssignment.value}, {AssignmentField.assignedBy.value}) VALUES (%s, %s, %s, %s, %s, %s)", (new_assignment.changeInterface, new_assignment.oldInterface, new_assignment.operator, new_assignment.dateAssignment, new_assignment.statusAssignment.value, new_assignment.assignedBy))
        res = cur.statusmessage
        if res == "INSERT 0 1":
            conn.commit()
            database.close_connection()
            return AssignmentModel.get_assignment(new_assignment.changeInterface, new_assignment.oldInterface, new_assignment.operator)
        else: 
            database.close_connection()
            return None
        
    def insert_assignments(data: List[dict]) -> int:
        """Create a list of assignments by performing a database query.
        
        Parameters
        ----------
        data: List[dict]
            List of dicts with the values of the assignments to be created.
        """
        total_inserted = 0
        data = [AssignmentEntity(**assignment) for assignment in data]
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        for assignment in data:
            cur.execute(f"INSERT INTO {TableDatabase.assignment.value} ({AssignmentField.changeInterface.value}, {AssignmentField.oldInterface.value}, {AssignmentField.operator.value}, {AssignmentField.dateAssignment.value}, {AssignmentField.statusAssignment.value}, {AssignmentField.assignedBy.value}) VALUES (%s, %s, %s, %s, %s, %s)", (assignment.changeInterface, assignment.oldInterface, assignment.operator, assignment.dateAssignment, assignment.statusAssignment.value, assignment.assignedBy))
            res = cur.statusmessage
            if res == "INSERT 0 1": total_inserted += 1
        conn.commit()
        database.close_connection()
        return total_inserted
    
    @staticmethod
    def delete_assignment(change_interface: int, old_interface: int, operator: str) -> bool:
        """Delete an assignment by performing a database query.
        
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
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(f"DELETE FROM {TableDatabase.assignment.value} WHERE {AssignmentField.changeInterface.value} = %s AND {AssignmentField.oldInterface.value} = %s AND {AssignmentField.operator.value} = %s", (change_interface, old_interface, operator))
        res = cur.statusmessage
        if res == "DELETE 1":
            conn.commit()
            database.close_connection()
            return True
        else: 
            database.close_connection()
            return False
        
    def delete_assignment_by_date_assignment(date_assignment: str) -> bool:
        """Delete an assignment by performing a database query.
        
        Parameters
        ----------
        date_assignment : str 
            The date of the assignment in format YYYY-MM-DD.
        """
        status = False
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(f"DELETE FROM {TableDatabase.assignment.value} WHERE {AssignmentField.dateAssignment.value} = %s", (date_assignment,))
        res = cur.statusmessage
        if "DELETE" in res: status = True
        conn.commit()
        database.close_connection()
        return status
    
    def update_operator_assignment(change_interface: int, old_interface: int, old_operator: str, new_operator: str, assigned_by: str) -> AssignmentEntity | None:
        """Update an assignment by performing a database query.
        
        Parameters
        ----------
        change_interface : int 
            The id of the interface with changes.
        old_interface : int 
            The id of the old interface.
        old_operator : str 
            The username of the old operator.
        new_operator : str 
            The username of the new operator.
        assigned_by : str
            The complete name of the operator who assigned the interface.
        """
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(f"UPDATE {TableDatabase.assignment.value} SET {AssignmentField.operator.value} = %s, {AssignmentField.assignedBy.value} = %s WHERE {AssignmentField.changeInterface.value} = %s AND {AssignmentField.oldInterface.value} = %s AND {AssignmentField.operator.value} = %s", (new_operator, assigned_by, change_interface, old_interface, old_operator))
        conn.commit()
        database.close_connection()
        return AssignmentModel.get_assignment(change_interface, old_interface, new_operator)
    
    def update_status_assignment(change_interface: int, old_interface: int, operator: str, status: Status) -> AssignmentEntity | None:
        """Update an assignment by performing a database query.
        
        Parameters
        ----------
        change_interface : int 
            The id of the interface with changes.
        old_interface : int 
            The id of the old interface.
        operator : str 
            The username of the operator.
        status : Status
            The new status of the assignment.
        """
        date_review = datetime.now().strftime("%Y-%m-%d")
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(f"UPDATE {TableDatabase.assignment.value} SET {AssignmentField.statusAssignment.value} = %s, {AssignmentField.dateReview.value} = %s WHERE {AssignmentField.changeInterface.value} = %s AND {AssignmentField.oldInterface.value} = %s AND {AssignmentField.operator.value} = %s", (status.value, date_review, change_interface, old_interface, operator))
        conn.commit()
        database.close_connection()
        return AssignmentModel.get_assignment(change_interface, old_interface, operator)