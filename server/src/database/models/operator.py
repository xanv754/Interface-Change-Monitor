from typing import List
from database.entities.operator import OperatorEntity
from database.constants.profile import TypeProfile
from database.constants.account import TypeStatusAccount
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
        
    @staticmethod
    def get_operator_by_profile(profile: TypeProfile) -> List[OperatorEntity]:
        """Obtain a list of all operators filter by profile by performing a database query.
        
        Parameters
        ----------
        profile : TypeProfile
            The profile of the operator.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM operator WHERE profile = %s", (profile,))
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
        
    @staticmethod
    def get_operator_by_status(status: TypeStatusAccount) -> List[OperatorEntity]:
        """Obtain a list of all operators filter by status account by performing a database query.
        
        Parameters
        ----------
        status : TypeStatusAccount
            The status of the operator.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM operator WHERE statusAccount = %s", (status,))
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
        
    @staticmethod
    def get_operator_by_delete() -> List[OperatorEntity]:
        """Obtain a list of all operators with deleteby performing a database query.
        
        Parameters
        ----------
        delete : bool
            The delete of the operator.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute("SELECT * FROM operator WHERE deleteOperator = %s", ('true',))
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
        
    def insert_operator(data: dict) -> OperatorEntity | None:
        """Create an operator by performing a database query.
        
        Parameters
        ----------
        data: dict
            Dict with the values of the operator to be created.
        """
        new_user = OperatorEntity(**data)
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute("INSERT INTO operator (username, name, lastname, password, profile, statusAccount, deleteOperator) VALUES (%s, %s, %s, %s, %s, %s, %s)", (new_user.username, new_user.name, new_user.lastname, new_user.password, new_user.profile.value, new_user.statusAccount.value, new_user.deleteOperator))
        res = cur.statusmessage
        if res == "INSERT 0 1":
            conn.commit()
            database.close_connection()
            return OperatorModel.get_operator(new_user.username)
        else: 
            database.close_connection()
            return None