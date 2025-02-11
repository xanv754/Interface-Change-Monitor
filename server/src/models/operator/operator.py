from typing import List
from constants import GTABLES, AccountType
from database import PostgresDatabase
from schemas import OperatorSchema
from utils import operator_to_dict


class Operator:
    username: str

    def __init__(self, username: str):
        self.username = username

    @staticmethod
    def get_all() -> List[dict]:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(f"SELECT * FROM {GTABLES.OPERATOR.value}")
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return operator_to_dict(result)
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def get_all_profile_active(profile: str) -> List[dict]:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"SELECT * FROM {GTABLES.OPERATOR.value} WHERE {OperatorSchema.STATUS_ACCOUNT.value} = %s AND {OperatorSchema.PROFILE.value} = %s",
                (AccountType.ACTIVE.value, profile),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return operator_to_dict(result)
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def get_all_inactive() -> List[dict]:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"SELECT * FROM {GTABLES.OPERATOR.value} WHERE {OperatorSchema.STATUS_ACCOUNT.value} = %s",
                (AccountType.INACTIVE.value,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return operator_to_dict(result)
        except Exception as e:
            print(e)
            return []

    @staticmethod
    def get_all_deleted() -> List[dict]:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"SELECT * FROM {GTABLES.OPERATOR.value} WHERE {OperatorSchema.STATUS_ACCOUNT.value} = %s",
                (AccountType.DELETED.value,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return operator_to_dict(result)
        except Exception as e:
            print(e)
            return []

    def get(self) -> List[dict]:
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"SELECT * FROM {GTABLES.OPERATOR.value} WHERE {OperatorSchema.USERNAME.value} = %s",
                (self.username,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return []
            return operator_to_dict([result])
        except Exception as e:
            print(e)
            return []

    def delete(self) -> bool:
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"DELETE FROM {GTABLES.OPERATOR.value} WHERE {OperatorSchema.USERNAME.value} = %s",
                (self.username,),
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
