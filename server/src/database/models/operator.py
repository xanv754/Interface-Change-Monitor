from typing import List
from database.entities.operator import OperatorEntity
from database.utils.database import Database

class OperatorModel:
    @staticmethod
    def get_operator(username: str) -> OperatorEntity | None:
        """Obtain an operator by performing a database query.
        
        Parameters
        ----------
        username : str 
            The username of the operator to be obtained.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM operator WHERE username = %s", (username,))
        res = cur.fetchone()
        database.close_connection()
        if res:
            data = dict(zip(OperatorEntity.model_fields.keys(), res))
            operator = OperatorEntity(**data)
            return operator
        else:
            return None

    @staticmethod   
    def get_operators() -> List[OperatorEntity]:
        """Obtain a list of all operators by performing a database query."""
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM operator")
        res = cur.fetchall()
        database.close_connection()
        if res:
            operators: List[OperatorEntity] = []
            for data in res:
                data = dict(zip(OperatorEntity.model_fields.keys(), data))
                operator = OperatorEntity(**data)
                operators.append(operator)
            return operators
        else:
            return []