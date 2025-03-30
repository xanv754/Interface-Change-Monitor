from typing import List
from constants.types import AccountType
from database.models.operator import OperatorModel
from schemas.operator import OperatorSchema, RegisterUserBody, UpdateUserRootBody
from utils.log import LogHandler
from utils.valid import ValidDataHandler
from utils import encrypt


class OperatorController:
    """Controller for all operations of operator table."""

    @staticmethod
    def register_operator(body: RegisterUserBody) -> bool:
        """Register a new operator in the system.

        Parameters
        ----------
        body : OperatorRegisterBody
            Data of the new operator.
        """
        try:
            body.profile = body.profile.upper()
            if not ValidDataHandler.profile_type(body.profile):
                raise Exception("Failed to register operator. Invalid profile type")
            if OperatorController.get_operator(body.username):
                raise Exception("Failed to register operator. Username not available")
            password_hash = encrypt.get_password_hash(body.password)
            return OperatorModel.register(
                username=body.username,
                name=body.name,
                lastname=body.lastname,
                password=password_hash,
                profile=body.profile,
                account=AccountType.ACTIVE.value,
            )
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False

    @staticmethod
    def get_operator(username: str, confidential: bool = True) -> OperatorSchema | None:
        """Obtain an operator object with all information of the operator.

        Parameters
        ----------
        username : str
            Operator's username.
        confidential : bool
            If True, the password is not returned.
        """
        try:
            return OperatorModel.get_by_username(
                username=username,
                confidential=confidential
            )
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_operators() -> List[OperatorSchema]:
        """Obtain a list of all operators (except those to be deleted) in the system."""
        try:
            return OperatorModel.get_all_without_deleted()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_operators_profile_active(profile: str) -> List[OperatorSchema]:
        """Obtain a list of all active operators filter by an profile type in the system.

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
            if not ValidDataHandler.profile_type(profile):
                raise Exception("Failed to get operators profile active. Invalid profile type")
            return OperatorModel.get_all_profile_active(profile)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def update_operator(body: UpdateUserRootBody) -> bool:
        """Update data of an operator in the system.

        Parameters
        ----------
        body : OperatorUpdateBody
            Data of the operator to update.
        """
        try:
            if not OperatorModel.get_by_username(username=body.username):
                raise Exception("Failed to update operator. Operator not found")
            body.account = body.account.upper()
            if not ValidDataHandler.account_type(body.account):
                raise Exception("Failed to update operator. Invalid account type")
            body.profile = body.profile.upper()
            if not ValidDataHandler.profile_type(body.profile):
                raise Exception("Failed to update operator. Invalid profile type")
            return OperatorModel.update(
                username=body.username,
                name=body.name,
                lastname=body.lastname,
                profile=body.profile,
                account=body.account,
            )
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False

    @staticmethod
    def update_password(username: str, password: str) -> bool:
        """Update password of an operator in the system.

        Parameters
        ----------
        username : str
            Username of the operator.
        password : str
            New password of the operator.
        """
        try:
            if not OperatorModel.get_by_username(username=username):
                raise Exception("Failed to update password of an operator. Operator not found")
            password_hash = encrypt.get_password_hash(password)
            return OperatorModel.update_password(username, password_hash)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False

    @staticmethod
    def delete_soft_operator(username: str) -> bool:
        """Delete an operator of soft mode in the system.

        Parameters
        ----------
        username : str
            Username of the operator.
        """
        try:
            if not OperatorModel.get_by_username(username):
                raise Exception("Failed to delete operator. Operator not found")
            return OperatorModel.delete(username)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
