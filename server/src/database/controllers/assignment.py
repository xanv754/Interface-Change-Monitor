from error import ErrorHandler, ErrorAssignmentHandler, CODEASSIGNMENT
from database.utils.json import assignment_to_json
from database.constants.types.assignment import Status
from database.models.assignment import AssignmentModel
from database.models.operator import OperatorModel
from database.utils import create

class AssignmentController:
    @staticmethod
    def get_assignment_by_id(operator: str, change_interface: int, old_interface: int) -> list | ErrorHandler:
        """Get an assignment by performing a database query.
        
        Parameters
        ----------
        operator : str
            The username of the operator.
        change_interface : int
            The id of the interface with changes.
        old_interface : int
            The id of the old interface.
        """
        try:
            return assignment_to_json([AssignmentModel.get_assignment(change_interface, old_interface, operator)])
        except Exception as e:
            error =  ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error

    @staticmethod
    def read_all_assignments() -> list | ErrorHandler:
        """Get all assignments.
        """
        try:
            return assignment_to_json(AssignmentModel.get_assignments())
        except Exception as e:
            error =  ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error

    @staticmethod
    def read_assignments_by_operator(operator: str) -> list | ErrorHandler:
        """Get all assignments by operator.
        
        Parameters
        ----------
        operator : str
            The operator's username.
        """
        try:
            if not OperatorModel.get_operator(operator):
                return ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_404_OPERATOR_NOT_FOUND)
            else:
                return assignment_to_json(AssignmentModel.get_assignments_by_operator(operator))
        except Exception as e:
            error =  ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
    
    @staticmethod
    def read_assignments_by_operator_pending(operator: str) -> list | ErrorHandler:
        """Get all assignments by operator and status assignment is 'PENDING'.
        
        Parameters
        ----------
        operator : str
            The operator's username.
        """
        try: 
            if not OperatorModel.get_operator(operator):
                return ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_404_OPERATOR_NOT_FOUND)
            else:
                return assignment_to_json(AssignmentModel.get_assignments_by_operator_and_status(operator, Status.PENDING))
        except Exception as e:
            error =  ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error

    @staticmethod
    def read_assignments_by_operator_review(operator: str) -> list | ErrorHandler:
        """Get all assignments by operator and status assignment is 'REVIEW'.
        
        Parameters
        ----------
        operator : str
            The operator's username.
        """
        try: 
            if not OperatorModel.get_operator(operator):
                return ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_404_OPERATOR_NOT_FOUND)
            else:
                return assignment_to_json(AssignmentModel.get_assignments_by_operator_and_status(operator, Status.REVIEW))
        except Exception as e:
            error =  ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    @staticmethod
    def read_assignments_by_operator_rediscover(operator: str) -> list | ErrorHandler:
        """Get all assignments by operator and status assignment is 'REDISCOVER'.
        
        Parameters
        ----------
        operator : str
            The operator's username.
        """
        try: 
            if not OperatorModel.get_operator(operator):
                return ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_404_OPERATOR_NOT_FOUND)
            else:
                return assignment_to_json(AssignmentModel.get_assignments_by_operator_and_status(operator, Status.REDISCOVER))
        except Exception as e:
            error =  ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    @staticmethod
    def read_assignments_by_date_assignment(date_assignment: str) -> list | ErrorHandler:
        """Get all assignments by date assignment by performing a database query.
        
        Parameters
        ----------
        date_assignment : str
            The date of the assignment in format YYYY-MM-DD.
        """
        try:
            return assignment_to_json(AssignmentModel.get_assignments_by_date_assignment(date_assignment))
        except Exception as e:
            error =  ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    @staticmethod
    def read_assignments_by_status(status: Status) -> list | ErrorHandler:
        """Get all assignments by status assignment by performing a database query.
        
        Parameters
        ----------
        status : Status
            The status of the assignment.
        """
        try:
            if not status in Status:
                return ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_STATUS_NO_VALID)
            else:
                return assignment_to_json(AssignmentModel.get_assignments_by_status(status))
        except Exception as e:
            error =  ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
    
    @staticmethod
    def read_assignment_by_assigned(assigned_by: str) -> list | ErrorHandler:
        """Get all assignments by assigned by performing a database query.
        
        Parameters
        ----------
        assigned_by : str
            The username of the operator.
        """
        try:
            return assignment_to_json(AssignmentModel.get_assignments_by_assigned(assigned_by))
        except Exception as e:
            error =  ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    @staticmethod
    def read_assignment_by_review(date_review: str) -> list | ErrorHandler:
        """Get all assignments by date review by performing a database query.
        
        Parameters
        ----------
        date_review : datetime
            The date of the review in format YYYY-MM-DD.
        """
        try:
            return assignment_to_json(AssignmentModel.get_assignments_by_review(date_review))
        except Exception as e:
            error =  ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    @staticmethod
    def create_assignment(body: dict) -> list | ErrorHandler:
        """Create an assignment by performing a database query.
        
        Parameters
        ----------
        data: dict
            Dict with the values of the assignment to be created.
        """
        try:
            return assignment_to_json(AssignmentModel.insert_assignment(body))
        except Exception as e:
            error =  ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    @staticmethod
    def create_assignments(body: list) -> int | ErrorHandler:
        """
        Create a list of assignments.

        Parameters
        ----------
        body: list
            List of dicts with the values of the assignments to be created.
        """
        try:
            total = AssignmentModel.insert_assignments(body)
            return total
        except Exception as e:
            error =  ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    @staticmethod
    def delete_assignment(operator: str, change_interface: str, old_interface: str) -> bool | ErrorHandler:
        """
        Delete an assignment.

        Parameters
        ----------
        operator: str
            The operator of the assignment.
        change_interface: str
            The id of the new interface.
        old_interface: str
            The id of the old interface.
        """
        try:
            return AssignmentModel.delete_assignment(operator, change_interface, old_interface)
        except Exception as e:
            error =  ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    @staticmethod
    def delete_assignments_by_date_assignment(date_assignment: str) -> bool | ErrorHandler:
        """
        Delete all assignments by date of assignment.

        Parameters
        ----------
        date_assignment: str
            The date of the assignment.
        """
        try:
            return AssignmentModel.delete_assignments_by_date_assignment(date_assignment)
        except Exception as e:
            error =  ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    @staticmethod
    def update_status_assignment(change_interface: int, old_interface: int, operator: str, status: str) -> list | ErrorHandler:
        """
        Update the status of an assignment.

        Parameters
        ----------
        change_interface: int
            The id of the new interface.
        old_interface: int
            The id of the old interface.
        operator: str
            The operator of the assignment.
        status: Status
            The new status of the assignment.
        """
        try:
            if not status in Status:
                return ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_400_STATUS_NO_VALID)
            else: 
                if not AssignmentModel.get_assignment(change_interface, old_interface, operator):
                    return ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_404_ASSIGNMENT_NOT_FOUND)
                else: return assignment_to_json([AssignmentModel.update_status_assignment(change_interface, old_interface, operator, status)])
        except Exception as e:
            error =  ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    @staticmethod
    def update_operator_assingment(change_interface: int, old_interface: int, old_operator: str, new_operator: str, assigned_by: str) -> list | ErrorHandler:
        """
        Update the operator of an assignment.

        Parameters
        ----------
        change_interface: int
            The id of the new interface.
        old_interface: int
            The id of the old interface.
        old_operator: str
            The operator of the old assignment.
        new_operator: str
            The operator of the new assignment.
        assigned_by: str
            The complete name of the operator who assigned the interface.
        """
        try:
            if not AssignmentModel.get_assignment(change_interface, old_interface, old_operator):
                return ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_404_ASSIGNMENT_NOT_FOUND)
            else: 
                if not OperatorModel.get_operator(new_operator):
                    return ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_404_OPERATOR_NOT_FOUND)
                else: return assignment_to_json([AssignmentModel.update_operator_assingment(change_interface, old_interface, old_operator, new_operator, assigned_by)])
        except Exception as e:
            error =  ErrorAssignmentHandler(CODEASSIGNMENT.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error