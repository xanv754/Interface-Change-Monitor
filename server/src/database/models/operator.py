from typing import List
from constants.types import AccountType
from database.constants.tables import Tables as GTABLES # Global Tables
from database.database import PostgresDatabase
from database.schemas.operator import OperatorSchemaDB
from schemas.operator import OperatorSchema
from utils.convert import OperatorResponse
from utils.log import LogHandler


class OperatorModel:
    """Model for all queries of the operator table."""

    @staticmethod
    def register(username: str, name: str, lastname: str, password: str, profile: str, account: str) -> bool:
        """Register a new operator in the database.

        Parameters
        ----------
        username : str
            Operator's username.
        name : str
            Operator's name.
        lastname : str
            Operator's lastname.
        password : str
            Operator's password.
        profile : str
            Operator's profile type.
        account :  str
            Operator's account status.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    INSERT INTO {GTABLES.OPERATOR.value} (
                        {OperatorSchemaDB.USERNAME.value},
                        {OperatorSchemaDB.NAME.value},
                        {OperatorSchemaDB.LASTNAME.value},
                        {OperatorSchemaDB.PASSWORD.value},
                        {OperatorSchemaDB.PROFILE.value},
                        {OperatorSchemaDB.STATUS_ACCOUNT.value}
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    username,
                    name,
                    lastname,
                    password,
                    profile.upper(),
                    account.upper(),
                ),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if status and status == "INSERT 0 1":
                return True
            else:
                return False

    @staticmethod
    def get_by_username(username: str, confidential: bool = True) -> OperatorSchema | None:
        """Get information about an operator.

        Parameters
        ----------
        username : str
            Operator's username.
        confidential : bool
            If True, the password is not returned.
        """
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT *
                    FROM
                        {GTABLES.OPERATOR.value}
                    WHERE
                        {OperatorSchemaDB.USERNAME.value} = %s
                """,
                (username,),
            )
            result = cursor.fetchone()
            database.close_connection()
            if not result:
                return None
            if confidential:
                operator = OperatorResponse.convert_to_dict([result])
            else:
                operator = OperatorResponse.convert_to_dict_complete([result])
            if len(operator) == 0: return None
            else: return operator[0]
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_all() -> List[OperatorSchema]:
        """Get all operators."""
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT *
                    FROM
                        {GTABLES.OPERATOR.value}
                """
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return OperatorResponse.convert_to_dict(result)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_all_without_deleted() -> List[OperatorSchema]:
        """Get all the operators in the database except the operators to be deleted."""
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT *
                    FROM
                        {GTABLES.OPERATOR.value}
                    WHERE
                        {OperatorSchemaDB.STATUS_ACCOUNT.value} != %s
                """,
                (AccountType.DELETED.value,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return OperatorResponse.convert_to_dict(result)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
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
                f"""
                    SELECT *
                    FROM
                        {GTABLES.OPERATOR.value}
                    WHERE
                        {OperatorSchemaDB.STATUS_ACCOUNT.value} = %s AND
                        {OperatorSchemaDB.PROFILE.value} = %s
                """,
                (AccountType.ACTIVE.value, profile.upper()),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return OperatorResponse.convert_to_dict(result)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_all_inactive() -> List[OperatorSchema]:
        """Get all inactive operators of the system."""
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT *
                    FROM
                        {GTABLES.OPERATOR.value}
                    WHERE
                        {OperatorSchemaDB.STATUS_ACCOUNT.value} = %s
                """,
                (AccountType.INACTIVE.value,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return OperatorResponse.convert_to_dict(result)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_all_deleted() -> List[OperatorSchema]:
        """Get all deleted operators of the system."""
        try:
            database = PostgresDatabase()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    SELECT *
                    FROM
                        {GTABLES.OPERATOR.value}
                    WHERE
                        {OperatorSchemaDB.STATUS_ACCOUNT.value} = %s
                """,
                (AccountType.DELETED.value,),
            )
            result = cursor.fetchall()
            database.close_connection()
            if not result:
                return []
            return OperatorResponse.convert_to_dict(result)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def update(username: str, name: str, lastname: str, profile: str, account: str) -> bool:
        """Update data of an operator existing in the database.

        Parameters
        ----------
        username : str
            Operator's username.
        name : str
            Operator's name.
        lastname : str
            Operator's lastname.
        profile : str
            Operator's profile type.
        account :  str
            Operator's account status.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    UPDATE
                        {GTABLES.OPERATOR.value}
                    SET
                        {OperatorSchemaDB.NAME.value} = %s,
                        {OperatorSchemaDB.LASTNAME.value} = %s,
                        {OperatorSchemaDB.PROFILE.value} = %s,
                        {OperatorSchemaDB.STATUS_ACCOUNT.value} = %s
                    WHERE
                        {OperatorSchemaDB.USERNAME.value} = %s
                """,
                (
                    name,
                    lastname,
                    profile,
                    account,
                    username,
                ),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if status and status == "UPDATE 1":
                return True
            else:
                return False

    @staticmethod
    def update_password(username: str, new_password: str) -> bool:
        """Update password of the operator.

        Parameters
        ----------
        username : str
            Operator's username.
        password : str
            New password operator.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    UPDATE
                        {GTABLES.OPERATOR.value}
                    SET
                        {OperatorSchemaDB.PASSWORD.value} = %s
                    WHERE
                        {OperatorSchemaDB.USERNAME.value} = %s
                """,
                (
                    new_password,
                    username,
                ),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if status and status == "UPDATE 1":
                return True
            else:
                return False

    @staticmethod
    def delete(username: str) -> bool:
        """Delete the operator by username.

        Parameters
        ----------
        username : str
            Operator's username.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                    DELETE FROM
                        {GTABLES.OPERATOR.value}
                    WHERE
                        {OperatorSchemaDB.USERNAME.value} = %s
                """,
                (username,),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            if status and status == "DELETE 1":
                return True
            else:
                return False
