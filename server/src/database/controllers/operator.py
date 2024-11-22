from error import ErrorHandler, ErrorOperatorHandler, ErrorCodeOperator
from database.constants.profile import TypeProfile
from database.constants.account import TypeStatusAccount
from database.models.operator import OperatorModel
from database.utils.json import operator_to_json
from database.utils import create


class OperatorController:
    @staticmethod
    def read_all_operators() -> list:
        """Get all operators, including the operator will be deleted"""
        try:
            return operator_to_json(OperatorModel.get_all_operators())
        except Exception as e:
            return create.log(e)

    @staticmethod
    def read_operators() -> list:
        """Get all operators, excluding the operator will be deleted"""
        try: 
            return operator_to_json(OperatorModel.get_operators())
        except Exception as e:
            return create.log(e)

    @staticmethod
    def read_operator(username: str) -> list:
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
            return create.log(e)

    @staticmethod
    def read_operators_by_profile(profile: str) -> list:
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
                raise ValueError(f"The profile {profile} is not valid.")
            return operator_to_json(OperatorModel.get_operators_by_profile(profile))
        except Exception as e:
            return create.log(e)

    @staticmethod
    def read_operators_by_status(status: str) -> list:
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
                raise ValueError(f"The status {status} is not valid.")
            return operator_to_json(OperatorModel.get_operators_by_status(status))
        except Exception as e:
            return create.log(e)

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
                return []
            # TODO: Create the hash password
            return operator_to_json(OperatorModel.insert_operator(body))
        except Exception as e:
            return create.log(e)
        
    @staticmethod
    def delete_operator_hard(username: str) ->  bool | ErrorHandler:
        """Delete an operator by performing a database query.

        Parameters
        ----------
        username : str
            The username of the operator to be deleted.
        """
        try:
            # if OperatorModel.get_operator(username):
            #     return OperatorModel.delete_operator(username)
            # else: 
                return ErrorOperatorHandler(ErrorCodeOperator.ERROR_10_OPERATOR_NOT_FOUND)
        except Exception as e:
            create.log(e)
            return ErrorOperatorHandler(500)
