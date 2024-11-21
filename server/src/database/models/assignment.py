from typing import List
from database.entities.assignment import AssignmentEntity
from database.utils.database import Database

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