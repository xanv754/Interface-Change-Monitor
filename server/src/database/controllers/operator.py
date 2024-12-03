from error import ErrorHandler, ErrorOperatorHandler, CODEOPERATOR
from database.entities.operator import OperatorField
from database.constants.types.operator import Profile, StatusAccount
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
            error =  ErrorOperatorHandler(CODEOPERATOR.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error

    @staticmethod
    def read_operators() -> list | ErrorHandler:
        """Get all operators, excluding the operator will be deleted"""
        try: 
            return operator_to_json(OperatorModel.get_operators())
        except Exception as e:
            error =  ErrorOperatorHandler(CODEOPERATOR.ERROR_500_UNKNOWN)
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
            error =  ErrorOperatorHandler(CODEOPERATOR.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error

    @staticmethod
    def read_operators_by_profile(profile: str) -> list | ErrorHandler:
        """Get all operators by profile.

        Parameters
        ----------
        profile: Profile
            The profile of the operator.
        """
        try:
            if not profile in Profile:
                return ErrorOperatorHandler(CODEOPERATOR.ERROR_400_PROFILE_NOT_VALID)
            return operator_to_json(OperatorModel.get_operators_by_profile(profile))
        except Exception as e:
            error =  ErrorOperatorHandler(CODEOPERATOR.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error

    @staticmethod
    def read_operators_by_status(status: str) -> list | ErrorHandler:
        """Get all operators by status account.

        Parameters
        ----------
        status: StatusAccount
            The status of the operator.
        """
        try:
            if (
                status not in StatusAccount.active.value
                or status not in StatusAccount.inactive.value
            ):
                return ErrorOperatorHandler(CODEOPERATOR.ERROR_400_STATUS_NOT_VALID)
            return operator_to_json(OperatorModel.get_operators_by_status(status))
        except Exception as e:
            error =  ErrorOperatorHandler(CODEOPERATOR.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
    
    @staticmethod
    def read_operators_by_delete() -> list | ErrorHandler:
        """Get all operators with delete equal to true."""
        try:
            return operator_to_json(OperatorModel.get_operators_by_delete())
        except Exception as e:
            error =  ErrorOperatorHandler(CODEOPERATOR.ERROR_500_UNKNOWN)
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
            if OperatorModel.get_operator(body[{OperatorField.username.value}]):
                return ErrorOperatorHandler(CODEOPERATOR.ERROR_400_ALREADY_EXISTS)
            # TODO: Create the hash password
            return operator_to_json(OperatorModel.insert_operator(body))
        except Exception as e:
            error =  ErrorOperatorHandler(CODEOPERATOR.ERROR_500_UNKNOWN)
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
                return ErrorOperatorHandler(CODEOPERATOR.ERROR_404_OPERATOR_NOT_FOUND)
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
                OperatorModel.update_delete_operator(username, True)
                return operator_to_json([OperatorModel.get_operator(username)])
            else:
                return ErrorOperatorHandler(CODEOPERATOR.ERROR_404_OPERATOR_NOT_FOUND)
        except Exception as e:
            create.log(e)
            return ErrorOperatorHandler(500)

    @staticmethod
    def delete_operators_by_delete() -> bool | ErrorHandler:
        """Delete all operators with the status delete operators equal to true by performing a database query."""
        try:
            return OperatorModel.delete_operators_by_status_delete()
        except Exception as e:
            create.log(e)
            return ErrorOperatorHandler(500)
        
    @staticmethod
    def update_name_operator(username: str, name: str) -> list | ErrorHandler:
        """Update the name of an operator by performing a database query.

        Parameters
        ----------
        username : str
            The username of the operator.
        name : str
            The new name of the operator.
        """
        try:
            if OperatorModel.get_operator(username):
                OperatorModel.update_name_operator(username, name)
                return operator_to_json([OperatorModel.get_operator(username)])
            else:
                return ErrorOperatorHandler(CODEOPERATOR.ERROR_404_OPERATOR_NOT_FOUND)
        except Exception as e:
            create.log(e)
            return ErrorOperatorHandler(500)
        
    @staticmethod
    def update_lastname_operator(username: str, lastname: str) -> list | ErrorHandler:
        """Update the lastname of an operator by performing a database query.

        Parameters
        ----------
        username : str
            The username of the operator.
        lastname : str
            The new lastname of the operator.
        """
        try:
            if OperatorModel.get_operator(username):
                OperatorModel.update_lastname_operator(username, lastname)
                return operator_to_json([OperatorModel.get_operator(username)])
            else:
                return ErrorOperatorHandler(CODEOPERATOR.ERROR_404_OPERATOR_NOT_FOUND)
        except Exception as e:
            create.log(e)
            return ErrorOperatorHandler(500)

    @staticmethod
    def update_password_operator(username: str, password: str) -> list | ErrorHandler:
        """Update the password of an operator by performing a database query.

        Parameters
        ----------
        username : str
            The username of the operator.
        password : str
            The new password of the operator.
        """
        try:
            if OperatorModel.get_operator(username):
                # TODO: Create the hash password
                OperatorModel.update_password_operator(username, password)
                return operator_to_json([OperatorModel.get_operator(username)])
            else:
                return ErrorOperatorHandler(CODEOPERATOR.ERROR_404_OPERATOR_NOT_FOUND)
        except Exception as e:
            create.log(e)
            return ErrorOperatorHandler(500)
        
    @staticmethod
    def update_profile_operator(username: str, profile: str) -> list | ErrorHandler:
        """Update the profile of an operator by performing a database query.

        Parameters
        ----------
        username : str
            The username of the operator.
        profile : str
            The new profile of the operator.
        """
        try:
            if OperatorModel.get_operator(username):
                if (
                    profile not in Profile.super_admin.value
                    or profile not in Profile.admin.value
                    or profile not in Profile.standard.value
                    or profile not in Profile.soport.name
                ):
                    return ErrorOperatorHandler(CODEOPERATOR.ERROR_400_PROFILE_NOT_VALID)
                OperatorModel.update_profile_operator(username, profile)
                return operator_to_json([OperatorModel.get_operator(username)])
            else:
                return ErrorOperatorHandler(CODEOPERATOR.ERROR_404_OPERATOR_NOT_FOUND)
        except Exception as e:
            create.log(e)
            return ErrorOperatorHandler(500)
        
    @staticmethod
    def update_status_account_operator(username: str, status: str) -> list | ErrorHandler:
        """Update the status account of an operator by performing a database query.

        Parameters
        ----------
        username : str
            The username of the operator.
        status : str
            The new status account of the operator.
        """
        try:
            if OperatorModel.get_operator(username):
                if (
                    status not in StatusAccount.active.value
                    or status not in StatusAccount.inactive.value
                ):
                    return ErrorOperatorHandler(CODEOPERATOR.ERROR_400_STATUS_NOT_VALID)
                OperatorModel.update_status_account_operator(username, status)
                return operator_to_json([OperatorModel.get_operator(username)])
            else:
                return ErrorOperatorHandler(CODEOPERATOR.ERROR_404_OPERATOR_NOT_FOUND)
        except Exception as e:
            create.log(e)
            return ErrorOperatorHandler(500)
        
    @staticmethod
    def restore_operator(username: str) ->  bool | ErrorHandler:
        """Change the status of delete of an operator to False by performing a database query.

        Parameters
        ----------
        username : str
            The username of the operator to be deleted.
        """
        try:
            if OperatorModel.get_operator(username):
                OperatorModel.update_delete_operator(username, False)
                return operator_to_json([OperatorModel.get_operator(username)])
            else:
                return ErrorOperatorHandler(CODEOPERATOR.ERROR_404_OPERATOR_NOT_FOUND)
        except Exception as e:
            create.log(e)
            return ErrorOperatorHandler(500)
