from error import ErrorHandler, ErrorOperatorHandler, STATUS
from database.constants.profile import TypeProfile
from database.constants.account import TypeStatusAccount
from database.models.operator import OperatorModel
from database.utils.json import operator_to_json
from database.utils import create


class OperatorController:
    @staticmethod
    def read_all_operators() -> list | ErrorHandler:
        """Get all operators, including the operator will be deleted"""
        try:
            return operator_to_json(OperatorModel.get_all_operators())
        except Exception as e:
            error =  ErrorOperatorHandler(STATUS.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error

    @staticmethod
    def read_operators() -> list | ErrorHandler:
        """Get all operators, excluding the operator will be deleted"""
        try: 
            return operator_to_json(OperatorModel.get_operators())
        except Exception as e:
            error =  ErrorOperatorHandler(STATUS.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error

    @staticmethod
    def read_operator(username: str) -> list | ErrorHandler:
        """Get an list with an unique operator.

        Parameters
        ----------
        username: str
            The username's operator.
        """
        try:
            operator = OperatorModel.get_operator(username)
            if operator: return operator_to_json([operator])
            else: return []
        except Exception as e:
            error =  ErrorOperatorHandler(STATUS.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error

    @staticmethod
    def read_operators_by_profile(profile: str) -> list | ErrorHandler:
        """Get all operators by profile.

        Parameters
        ----------
        profile: TypeProfile
            The profile of the operator.
        """
        try:
            if (
                profile not in TypeProfile.super_admin.value
                or profile not in TypeProfile.admin.value
                or profile not in TypeProfile.standard.value
                or profile not in TypeProfile.soport.name
            ):
                return ErrorOperatorHandler(STATUS.ERROR_400_PROFILE_NOT_VALID)
            return operator_to_json(OperatorModel.get_operators_by_profile(profile))
        except Exception as e:
            error =  ErrorOperatorHandler(STATUS.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error

    @staticmethod
    def read_operators_by_status(status: str) -> list | ErrorHandler:
        """Get all operators by status account.

        Parameters
        ----------
        status: TypeStatusAccount
            The status of the operator.
        """
        try:
            if (
                status not in TypeStatusAccount.active.value
                or status not in TypeStatusAccount.inactive.value
            ):
                return ErrorOperatorHandler(STATUS.ERROR_400_STATUS_NOT_VALID)
            return operator_to_json(OperatorModel.get_operators_by_status(status))
        except Exception as e:
            error =  ErrorOperatorHandler(STATUS.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error

    @staticmethod
    def create_operator(body: dict) -> list | ErrorHandler:
        """Create an operator.

        Parameters
        ----------
        body: dict
            Dict with the values of the operator to be created.
        """
        try:
            if OperatorModel.get_operator(body["username"]):
                return ErrorOperatorHandler(STATUS.ERROR_400_ALREADY_EXISTS)
            # TODO: Create the hash password
            return operator_to_json(OperatorModel.insert_operator(body))
        except Exception as e:
            error =  ErrorOperatorHandler(STATUS.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    @staticmethod
    def delete_operator_hard(username: str) ->  bool | ErrorHandler:
        """Delete an operator by performing a database query.

        Parameters
        ----------
        username : str
            The username of the operator to be deleted.
        """
        try:
            if OperatorModel.get_operator(username):
                return OperatorModel.delete_operator(username)
            else:
                return ErrorOperatorHandler(STATUS.ERROR_404_OPERATOR_NOT_FOUND)
        except Exception as e:
            create.log(e)
            return ErrorOperatorHandler(500)
        
    @staticmethod
    def delete_operator_soft(username: str) ->  bool | ErrorHandler:
        """Change the status of delete of an operator to True by performing a database query.

        Parameters
        ----------
        username : str
            The username of the operator to be deleted.
        """
        try:
            if OperatorModel.get_operator(username):
                pass
            else:
                return ErrorOperatorHandler(STATUS.ERROR_404_OPERATOR_NOT_FOUND)
        except Exception as e:
            create.log(e)
            return ErrorOperatorHandler(500)
