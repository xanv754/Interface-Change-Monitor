from typing import List
from icm.access.querys.query import Query
from icm.access.utils.adapter import AdapterUser
from icm.access.models.user import UserModel
from icm.constants import UserStatusTypes, UserField
from icm.data import TableNames
from icm.utils import log


class UserQuery(Query):
    """Class to manage user query."""

    def __init__(self, uri: str | None = None):
        super().__init__(uri)

    def insert(self, new_user: UserModel) -> bool:
        """Insert user in database.
        
        Parameters
        ----------
        new_user : UserModel
            User to insert.

        Returns
        -------
        bool
            True if the user was inserted successfully, False otherwise.
        """
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            cursor.execute(
                f"""
                    INSERT INTO {TableNames.USERS} (
                        {UserField.USERNAME},
                        {UserField.PASSWORD},
                        {UserField.NAME},
                        {UserField.LASTNAME},
                        {UserField.STATUS},
                        {UserField.ROLE}
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s
                    )
                """,
                (
                    new_user.username.lower(),
                    new_user.password,
                    new_user.name.capitalize(),
                    new_user.lastname.capitalize(),
                    new_user.status.upper(),
                    new_user.role.upper()
                )
            )
            self.database.get_connection().commit()
            self.database.close_connection()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User query error. Failed to insert user. {error}")
            return False
        else:
            return True
        
    def update(self, user: UserModel) -> bool:
        """Update user in database. Without password.
        
        Parameters
        ----------
        user : UserModel
            User to update.

        Returns
        -------
        bool
            True if the user was updated successfully, False otherwise.
        """
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            cursor.execute(
                f"""
                    UPDATE 
                        {TableNames.USERS}
                    SET 
                        {UserField.NAME} = %s,
                        {UserField.LASTNAME} = %s,
                        {UserField.STATUS} = %s,
                        {UserField.ROLE} = %s,
                        {UserField.UPDATED_AT} = NOW()
                    WHERE 
                        {UserField.USERNAME} = %s
                """,
                (
                    user.name.capitalize(),
                    user.lastname.capitalize(),
                    user.status.upper(),
                    user.role.upper(),
                    user.username
                )
            )
            self.database.get_connection().commit()
            self.database.close_connection()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User query error. Failed to update user. {error}")
            return False
        else:
            return True
        
    def update_password(self, username: str, password: str) -> bool:
        """Update password in database.
        
        Parameters
        ----------
        username : str
            Username to update password.
        password : str
            Password to update.

        Returns
        -------
        bool
            True if the password was updated successfully, False otherwise.
        """
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            cursor.execute(
                f"""
                    UPDATE 
                        {TableNames.USERS}
                    SET 
                        {UserField.PASSWORD} = %s
                    WHERE 
                        {UserField.USERNAME} = %s
                """,
                (password, username)
            )
            self.database.get_connection().commit()
            self.database.close_connection()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User query error. Failed to update password. {error}")
            return False
        else:
            return True
        
    def delete(self, usernames: List[str]) -> bool:
        """Delete users.
        
        Parameters
        ----------
        usernames : List[str]
            Usernames to delete.

        Returns
        -------
        bool
            True if the users were deleted successfully, False otherwise.
        """
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            for username in usernames:
                cursor.execute(
                    f"""
                        DELETE FROM {TableNames.USERS}
                        WHERE {UserField.USERNAME} = %s
                    """,
                    (username,)
                )
            self.database.get_connection().commit()
            self.database.close_connection()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User query error. Failed to delete users. {error}")
            return False
        else:
            return True
        
    def get(self, username: str) -> UserModel | None:
        """Get a user.
        
        Parameters
        ----------
        username : str
            Username to get user.

        Returns
        -------
        UserModel
            User.
        """
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            cursor.execute(
                f"""
                    SELECT
                        *
                    FROM
                        {TableNames.USERS}
                    WHERE
                        {UserField.USERNAME} = %s
                """,
                (username,)
            )
            response = cursor.fetchone()
            self.database.close_connection()
            user = AdapterUser.response([response])
            if user: return user[0]
            return None
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User service error. Failed to get user by username. {error}")
            return None
        
    def get_all(self) -> List[UserModel]:
        """Get all users."""
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            cursor.execute(
                f"""
                    SELECT
                        *
                    FROM
                        {TableNames.USERS}
                """
            )
            response = cursor.fetchall()
            self.database.close_connection()
            users = AdapterUser.response(response)
            return users
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User service error. Failed to get users. {error}")
            return []
        
    def get_users(self) -> List[UserModel]:
        """Get users without deleted."""
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            cursor.execute(
                f"""
                    SELECT
                        *
                    FROM
                        {TableNames.USERS}
                    WHERE
                        {UserField.STATUS} != '{UserStatusTypes.DELETED}'
                """
            )
            response = cursor.fetchall()
            self.database.close_connection()
            users = AdapterUser.response(response)
            return users
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User service error. Failed to get users. {error}")
            return []
        
    def get_deleted(self) -> List[UserModel]:
        """Get deleted users."""
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            cursor.execute(
                f"""
                    SELECT
                        *
                    FROM
                        {TableNames.USERS}
                    WHERE
                        {UserField.STATUS} = '{UserStatusTypes.DELETED}'
                """
            )
            response = cursor.fetchall()
            self.database.close_connection()
            users = AdapterUser.response(response)
            return users
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User service error. Failed to get users. {error}")
            return []
        
    def get_users_by_category(self, status: str, role: str) -> List[UserModel]:
        """Get users by a category. The category is a status with a role.
        
        Parameters
        ----------
        status : str
            Status to get users. The status can be ACTIVE, INACTIVE or DELETED.
        role : str
            Role to get users. The role can be ADMIN, ROOT, USER or SOPORT.
        """
        try:
            if not self.database.connected:
                self.database.open_connection()
            cursor = self.database.get_cursor()
            cursor.execute(
                f"""
                    SELECT
                        *
                    FROM
                        {TableNames.USERS}
                    WHERE
                        {UserField.STATUS} = %s AND
                        {UserField.ROLE} = %s
                """,
                (status, role)
            )
            response = cursor.fetchall()
            self.database.close_connection()
            users = AdapterUser.response(response)
            return users
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User service error. Failed to get users. {error}")
            return []
        