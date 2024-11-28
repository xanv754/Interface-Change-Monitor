from typing import List
from database.constants.fields import OperatorFieldsDatabase
from database.constants.tables import NameTablesDatabase
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
        cur.execute(f"SELECT * FROM {NameTablesDatabase.operator.value} WHERE {OperatorFieldsDatabase.username.value} = %s", (username,))
        res = cur.fetchone()
        database.close_connection()
        if res:
            data = dict(zip(OperatorEntity.model_fields.keys(), res))
            operator = OperatorEntity(**data)
            return operator
        else:
            return None

    @staticmethod
    def get_all_operators() -> List[OperatorEntity]:
        """Obtain a list of all operators (include the operators with delete equal to true) by performing a database query."""
        database = Database()
        cur = database.get_cursor()
        cur.execute(f"SELECT * FROM {NameTablesDatabase.operator.value}")
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
    def get_operators() -> List[OperatorEntity]:
        """Obtain a list of all operators by performing a database query."""
        database = Database()
        cur = database.get_cursor()
        cur.execute(f"SELECT * FROM {NameTablesDatabase.operator.value} WHERE {OperatorFieldsDatabase.deleteOperator.value} = %s", ("false",))
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
    def get_operators_by_profile(profile: TypeProfile) -> List[OperatorEntity]:
        """Obtain a list of all operators filter by profile by performing a database query.

        Parameters
        ----------
        profile : TypeProfile
            The profile of the operator.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute(f"SELECT * FROM {NameTablesDatabase.operator.value} WHERE {OperatorFieldsDatabase.profile.value} = %s", (profile,))
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
    def get_operators_by_status(status: TypeStatusAccount) -> List[OperatorEntity]:
        """Obtain a list of all operators filter by status account by performing a database query.

        Parameters
        ----------
        status : TypeStatusAccount
            The status of the operator.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute(f"SELECT * FROM {NameTablesDatabase.operator.value} WHERE {OperatorFieldsDatabase.statusAccount.value} = %s", (status,))
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
    def get_operators_by_delete() -> List[OperatorEntity]:
        """Obtain a list of all operators with deleteby performing a database query.

        Parameters
        ----------
        delete : bool
            The delete of the operator.
        """
        database = Database()
        cur = database.get_cursor()
        cur.execute(f"SELECT * FROM {NameTablesDatabase.operator.value} WHERE {OperatorFieldsDatabase.deleteOperator.value} = %s", ("true",))
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
        data["statusAccount"] = TypeStatusAccount.active.value
        data["deleteOperator"] = False
        new_user = OperatorEntity(**data)
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(
            f"INSERT INTO {NameTablesDatabase.operator.value} ({OperatorFieldsDatabase.username.value}, {OperatorFieldsDatabase.name.value}, {OperatorFieldsDatabase.lastname.value}, {OperatorFieldsDatabase.password.value}, {OperatorFieldsDatabase.profile.value}, {OperatorFieldsDatabase.statusAccount.value}, {OperatorFieldsDatabase.deleteOperator.value}) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                new_user.username,
                new_user.name,
                new_user.lastname,
                new_user.password,
                new_user.profile.value,
                new_user.statusAccount.value,
                new_user.deleteOperator,
            ),
        )
        res = cur.statusmessage
        if res == "INSERT 0 1":
            conn.commit()
            database.close_connection()
            return OperatorModel.get_operator(new_user.username)
        else:
            database.close_connection()
            return None

    def delete_operator(username: str) -> bool:
        """Delete an operator by performing a database query.

        Parameters
        ----------
        username : str
            The username of the operator to be deleted.
        """
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(f"DELETE FROM {NameTablesDatabase.operator.value} WHERE {OperatorFieldsDatabase.username.value} = %s", (username,))
        res = cur.statusmessage
        if res == "DELETE 1":
            conn.commit()
            database.close_connection()
            return True
        else:
            database.close_connection()
            return False

    def delete_operators_by_status_delete() -> bool:
        """Delete all operators with the status delete operators equal to true by performing a database query."""
        status = False
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(f"DELETE FROM {NameTablesDatabase.operator.value} WHERE {OperatorFieldsDatabase.deleteOperator.value} = %s", ("true",))
        res = cur.statusmessage
        if "DELETE" in res:
            status = True
        conn.commit()
        database.close_connection()
        return status

    def update_name_operator(username: str, name: str) -> OperatorEntity | None:
        """Update the name of an operator by performing a database query.

        Parameters
        ----------
        username : str
            The username of the operator.
        name : str
            The new name of the operator.
        """
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(
            f"UPDATE {NameTablesDatabase.operator.value} SET {OperatorFieldsDatabase.name.value} = %s WHERE {OperatorFieldsDatabase.username.value} = %s", (name, username)
        )
        conn.commit()
        database.close_connection()
        return OperatorModel.get_operator(username)

    def update_lastname_operator(username: str, lastname: str) -> OperatorEntity | None:
        """Update the lastname of an operator by performing a database query.

        Parameters
        ----------
        username : str
            The username of the operator.
        lastname : str
            The new lastname of the operator.
        """
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(
            f"UPDATE {NameTablesDatabase.operator.value} SET {OperatorFieldsDatabase.lastname.value} = %s WHERE {OperatorFieldsDatabase.username.value} = %s",
            (lastname, username),
        )
        conn.commit()
        database.close_connection()
        return OperatorModel.get_operator(username)

    def update_password_operator(username: str, password: str) -> OperatorEntity | None:
        """Update the password of an operator by performing a database query.

        Parameters
        ----------
        username : str
            The username of the operator.
        password : str
            The new password of the operator.
        """
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(
            f"UPDATE {NameTablesDatabase.operator.value} SET {OperatorFieldsDatabase.password.value} = %s WHERE {OperatorFieldsDatabase.username.value} = %s",
            (password, username),
        )
        conn.commit()
        database.close_connection()
        return OperatorModel.get_operator(username)

    def update_profile_operator(
        username: str, profile: TypeProfile
    ) -> OperatorEntity | None:
        """Update the profile of an operator by performing a database query.

        Parameters
        ----------
        username : str
            The username of the operator.
        profile : TypeProfile
            The new profile of the operator.
        """
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(
            f"UPDATE {NameTablesDatabase.operator.value} SET {OperatorFieldsDatabase.profile.value} = %s WHERE {OperatorFieldsDatabase.username.value} = %s", (profile, username)
        )
        conn.commit()
        database.close_connection()
        return OperatorModel.get_operator(username)

    def update_status_account_operator(
        username: str, status: TypeStatusAccount
    ) -> OperatorEntity | None:
        """Update the status account of an operator by performing a database query.

        Parameters
        ----------
        username : str
            The username of the operator.
        status : TypeStatusAccount
            The new status account of the operator.
        """
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(
            f"UPDATE {NameTablesDatabase.operator.value} SET {OperatorFieldsDatabase.statusAccount.value} = %s WHERE {OperatorFieldsDatabase.username.value} = %s",
            (status, username),
        )
        conn.commit()
        database.close_connection()
        return OperatorModel.get_operator(username)

    def update_delete_operator(username: str, delete: bool) -> OperatorEntity | None:
        """Update the delete of an operator by performing a database query.

        Parameters
        ----------
        username : str
            The username of the operator.
        delete : bool
            The new delete of the operator.
        """
        database = Database()
        conn = database.get_connection()
        cur = database.get_cursor()
        cur.execute(
            f"UPDATE {NameTablesDatabase.operator.value} SET {OperatorFieldsDatabase.deleteOperator.value} = %s WHERE {OperatorFieldsDatabase.username.value} = %s",
            (delete, username),
        )
        conn.commit()
        database.close_connection()
        return OperatorModel.get_operator(username)
