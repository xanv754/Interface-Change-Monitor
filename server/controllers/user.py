from typing import Tuple, List
from constants.code import ResponseCode
from database.querys.user import UserQuery
from models.user import UserModel
from utils.validate import Validate
from utils.log import log


class UserController:
    """Class to manage user controller."""

    @staticmethod
    def new_user(new_user: UserModel) -> ResponseCode:
        """Insert a new user.
        
        Parameters
        ----------
        new_user : UserModel
            User to insert.
        """
        try:
            query = UserQuery()
            if query.get(username=new_user.username):
                return ResponseCode(status=400, message="Invalid username")
            if not Validate.role(role=new_user.role):
                return ResponseCode(status=400, message="Invalid role")
            if not Validate.status(status=new_user.status):
                return ResponseCode(status=400, message="Invalid status")
            status_operation = query.insert(new_user=new_user)
            if not status_operation:
                return ResponseCode(status=400, message="Failed to insert user")
            return ResponseCode(status=201)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User controller error. Failed to insert a new user. {error}")
            return ResponseCode(status=500)
        
    @staticmethod
    def update_user(user: UserModel) -> ResponseCode:
        """Update a user.
        
        Parameters
        ----------
        user : UserModel
            User to update.
        """
        try:
            query = UserQuery()
            if not query.get(username=user.username):
                return ResponseCode(status=404, message="User not found to update")
            if not Validate.role(role=user.role):
                return ResponseCode(status=400, message="Invalid role")
            if not Validate.status(status=user.status):
                return ResponseCode(status=400, message="Invalid status")
            status_operation = query.update(user=user)
            if not status_operation:
                return ResponseCode(status=500, message="Failed to update user")
            return ResponseCode(status=200)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User controller error. Failed to update a user. {error}")
            return ResponseCode(status=500)
        
    @staticmethod
    def update_password(username: str, password: str) -> ResponseCode:
        """Update password of a user.
        
        Parameters
        ----------
        username : str
            Username to update password.
        password : str
            Password to update.
        """
        try:
            query = UserQuery()
            if not query.get(username=username):
                return ResponseCode(status=404, message="User not found to update")
            status_operation = query.update_password(username=username, password=password)
            if not status_operation:
                return ResponseCode(status=500, message="Failed to update password")
            return ResponseCode(status=200)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User controller error. Failed to update password. {error}")
            return ResponseCode(status=500)
        
    @staticmethod
    def get_user(username: str) -> Tuple[ResponseCode, UserModel | None]:
        """Get a user.
        
        Parameters
        ----------
        username : str
            Username to get user.

        Returns
        -------
        Tuple[ResponseCode, UserModel | None]
            Response code and user.
        """
        try:
            query = UserQuery()
            user = query.get(username=username)
            if not user:
                return ResponseCode(status=404, message="User not found"), None
            return ResponseCode(status=200), user
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User controller error. Failed to get a user. {error}")
            return ResponseCode(status=500), None
        
    @staticmethod
    def get_all_users() -> Tuple[ResponseCode, List[UserModel]]:
        """Get all users.
        
        Returns
        -------
        Tuple[ResponseCode, List[UserModel]]
            Response code and list of users.
        """
        try:
            query = UserQuery()
            users = query.get_all()
            if not users:
                return ResponseCode(status=404, message="Users not found"), []
            return ResponseCode(status=200), users
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User controller error. Failed to get all users. {error}")
            return ResponseCode(status=500), []
        
    @staticmethod
    def get_users() -> Tuple[ResponseCode, List[UserModel]]:
        """Get users without deleted."""
        try:
            query = UserQuery()
            users = query.get_users()
            if not users:
                return ResponseCode(status=404, message="Users not found"), []
            return ResponseCode(status=200), users
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User controller error. Failed to get users. {error}")
            return ResponseCode(status=500), []
        
    @staticmethod
    def get_deleted_users() -> Tuple[ResponseCode, List[UserModel]]:
        """Get deleted users."""
        try:
            query = UserQuery()
            users = query.get_deleted()
            if not users:
                return ResponseCode(status=404, message="Users not found"), []
            return ResponseCode(status=200), users
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User controller error. Failed to get users. {error}")
            return ResponseCode(status=500), []
        
    @staticmethod
    def get_users_by_category(status: str, role: str) -> Tuple[ResponseCode, List[UserModel]]:
        """Get users by a category.
        
        Parameters
        ----------
        status : str
            Status to get users. The status can be ACTIVE, INACTIVE or DELETED.
        role : str
            Role to get users. The role can be ADMIN, ROOT, USER or SOPORT.

        Returns
        -------
        Tuple[ResponseCode, List[UserModel]]
            Response code and list of users.
        """
        try:
            query = UserQuery()
            if not Validate.status(status=status):
                return ResponseCode(status=400, message="Invalid status"), []
            if not Validate.role(role=role):
                return ResponseCode(status=400, message="Invalid role"), []
            users = query.get_users_by_category(status=status, role=role)
            if not users:
                return ResponseCode(status=404, message="Users not found"), []
            return ResponseCode(status=200), users
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User controller error. Failed to get users by category. {error}")
            return ResponseCode(status=500), []