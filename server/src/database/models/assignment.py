from typing import List
from database.entities.assignment import AssignmentEntity
from database.utils.database import Database

class AssignmentModel:
    @staticmethod
    def get_assignment(interface_today: int, interface_yesterday: int, operator: str) -> AssignmentEntity | None:
        """Obtain an assignment by performing a database query.
        
        Parameters
        ----------
        interface_today : int
            The id of the interface with changes.
        interface_yesterday : int
            The id of the old interface.
        operator : str
            The username of the operator.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM assignment WHERE idInterfaceToday = %s AND idInterfaceYesterday = %s AND operator = %s", (interface_today, interface_yesterday, operator))
        res = cur.fetchone()
        database.close_connection()
        if res:
            data = dict(zip(AssignmentEntity.model_fields.keys(), res))
            assignment = AssignmentEntity(**data)
            return assignment
        else:
            return None