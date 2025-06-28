from typing import Tuple, List
from access.querys.user import UserQuery
from business.libs.code import ResponseCode
from business.controllers.config import ConfigController
from business.controllers.security import SecurityController
from business.models.user import UserModel, UserLoggedModel, UpdateUserModel
from constants.types import RoleTypes, UserStatusTypes
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
            security = SecurityController()
            hashed_password = security.create_password_hash(password=new_user.password)
            new_user.password = hashed_password
            status_operation = query.insert(new_user=new_user)
            if not status_operation:
                return ResponseCode(status=400, message="Failed to insert user")
            return ResponseCode(status=201)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User controller error. Failed to insert a new user. {error}")
            return ResponseCode(status=500)
        
    @staticmethod
    def update_user(update_user: UpdateUserModel) -> ResponseCode:
        """Update a user.
        
        Parameters
        ----------
        user : UserModel
            User to update.
        """
        try:
            query = UserQuery()
            if not query.get(username=update_user.username):
                return ResponseCode(status=404, message="User not found to update")
            if not Validate.role(role=update_user.role):
                return ResponseCode(status=400, message="Invalid role")
            if not Validate.status(status=update_user.status):
                return ResponseCode(status=400, message="Invalid status")
            user = UserModel(
                username=update_user.username,
                password="",
                name=update_user.name,
                lastname=update_user.lastname,
                status=update_user.status,
                role=update_user.role,
                created_at=None,
                updated_at=None
            )
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
            security = SecurityController()
            hashed_password = security.create_password_hash(password=password)
            status_operation = query.update_password(username=username, password=hashed_password)
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
    def get_user_logged(username: str) -> Tuple[ResponseCode, UserLoggedModel | None]:
        """Get user logged.
        
        Parameters
        ----------
        username : str
            Username to get user logged.

        Returns
        -------
        Tuple[ResponseCode, UserLoggedModel | None]
            Response code and user logged.
        """
        try:
            query = UserQuery()
            user = query.get(username=username)
            if not user:
                return ResponseCode(status=404, message="User not found"), None
            config = ConfigController.get_config()
            if user.status == UserStatusTypes.ACTIVE and user.role == RoleTypes.ROOT:
                can_assign = config.can_assign.root
                can_receive_assignment = config.can_receive_assignment.root
                view_information_global = config.view_information_global.root
            elif user.status == UserStatusTypes.ACTIVE and user.role == RoleTypes.ADMIN:
                can_assign = config.can_assign.admin
                can_receive_assignment = config.can_receive_assignment.admin
                view_information_global = config.view_information_global.admin
            elif user.status == UserStatusTypes.ACTIVE and user.role == RoleTypes.USER:
                can_assign = config.can_assign.user
                can_receive_assignment = config.can_receive_assignment.user
                view_information_global = config.view_information_global.user
            elif user.status == UserStatusTypes.ACTIVE and user.role == RoleTypes.SOPORT:
                can_assign = config.can_assign.soport
                can_receive_assignment = config.can_receive_assignment.soport
                view_information_global = config.view_information_global.soport
            else:
                can_assign = False
                can_receive_assignment = False
                view_information_global = False
            user_logged = UserLoggedModel(
                username=user.username,
                name=user.name,
                lastname=user.lastname,
                status=user.status,
                role=user.role,
                can_assign=can_assign,
                can_receive_assignment=can_receive_assignment,
                view_information_global=view_information_global
            )
            return ResponseCode(status=200), user_logged
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User controller error. Failed to get a user logged. {error}")
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
            if not users: return ResponseCode(status=200), []
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
            if not users: return ResponseCode(status=200), []
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
            if not users: return ResponseCode(status=200), []
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
                return ResponseCode(status=200), []
            return ResponseCode(status=200), users
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"User controller error. Failed to get users by category. {error}")
            return ResponseCode(status=500), []