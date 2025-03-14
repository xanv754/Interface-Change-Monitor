from typing import List
from constants import AccountType
from database import PostgresDatabase, GTABLES, OperatorSchemaDB
from schemas import OperatorSchema
from utils import operator_to_dict, operator_complete_to_dict, Log


class Operator:
    username: str

    def __init__(self, username: str):
        self.username = username.lower()

    @staticmethod
    def get_all() -> List[OperatorSchema]:
        """Get all operators of the system."""
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(f"""SELECT * FROM {GTABLES.OPERATOR.value}""")
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return operator_to_dict(result)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []
        
    @staticmethod
    def get_all_without_deleted() -> List[OperatorSchema]:
        """Get all the operators in the system except the operators to be deleted."""
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.OPERATOR.value} 
                WHERE {OperatorSchemaDB.STATUS_ACCOUNT.value} != %s""",
                (AccountType.DELETED.value,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return operator_to_dict(result)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    @staticmethod
    def get_all_profile_active(profile: str) -> List[OperatorSchema]:
        """Get all active operators filtered by profile.
        
        Parameters
        ----------
        profile : str
            Profile of the operators.
            - **ROOT:** User with root privileges.
            - **ADMIN:** User with admin privileges.
            - **STANDARD:** User with standard privileges.
            - **SOPORT:** User with support privileges.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.OPERATOR.value} 
                WHERE {OperatorSchemaDB.STATUS_ACCOUNT.value} = %s AND 
                {OperatorSchemaDB.PROFILE.value} = %s""",
                (AccountType.ACTIVE.value, profile.upper()),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return operator_to_dict(result)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    @staticmethod
    def get_all_inactive() -> List[OperatorSchema]:
        """Get all inactive operators of the system."""
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.OPERATOR.value} 
                WHERE {OperatorSchemaDB.STATUS_ACCOUNT.value} = %s""",
                (AccountType.INACTIVE.value,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return operator_to_dict(result)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    @staticmethod
    def get_all_deleted() -> List[OperatorSchema]:
        """Get all deleted operators of the system."""
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.OPERATOR.value} 
                WHERE {OperatorSchemaDB.STATUS_ACCOUNT.value} = %s""",
                (AccountType.DELETED.value,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return operator_to_dict(result)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    def get(self, confidential: bool = True) -> OperatorSchema | None:
        """Get info of the operator. \n
        _Note:_ Its necessary declare the username in the constructor.

        Parameters
        ----------
        confidential : bool
            If True, the password is not returned.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.OPERATOR.value} 
                WHERE {OperatorSchemaDB.USERNAME.value} = %s""",
                (self.username,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            if confidential: operator = operator_to_dict([result])
            else: operator = operator_complete_to_dict([result])
            if len(operator) == 0:
                return None
            return operator[0]
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None
        
    def update_password(self, password: str) -> bool:
        """Update password of the operator. \n
        _Note:_ Its necessary declare the username in the constructor.

        Parameters
        ----------
        password : str
            New password of the operator.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""UPDATE {GTABLES.OPERATOR.value} 
                SET {OperatorSchemaDB.PASSWORD.value} = %s
                WHERE {OperatorSchemaDB.USERNAME.value} = %s""",
                (
                    password,
                    self.username,
                ),
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
        """Delete the operator with the given username. \n
        _Note:_ Its necessary declare the username in the constructor.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""DELETE FROM {GTABLES.OPERATOR.value} 
                WHERE {OperatorSchemaDB.USERNAME.value} = %s""",
                (self.username,),
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
