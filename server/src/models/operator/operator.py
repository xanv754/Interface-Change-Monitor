from typing import List
from constants import AccountType
from database import PostgresDatabase, GTABLES, OperatorSchemaDB
from schemas import OperatorSchema
from utils import operator_to_dict, operator_complete_to_dict, Log


class Operator:
    username: str

    def __init__(self, username: str):
        self.username = username

    @staticmethod
    def get_all() -> List[OperatorSchema]:
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
    def get_all_profile_active(profile: str) -> List[OperatorSchema]:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""SELECT * FROM {GTABLES.OPERATOR.value} 
                WHERE {OperatorSchemaDB.STATUS_ACCOUNT.value} = %s AND 
                {OperatorSchemaDB.PROFILE.value} = %s""",
                (AccountType.ACTIVE.value, profile),
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

    def delete(self) -> bool:
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
