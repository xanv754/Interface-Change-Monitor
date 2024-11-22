from database.utils.json import assignment_to_json
from database.models.assignment import AssignmentModel

class AssignmentController:
    @staticmethod
    def get_assignments_by_operator(operator: str):
        """Get all assignments by operator.
        
        Parameters
        ----------
        operator : str
            The operator's username.
        """
        AssignmentModel.get_assignments_by_operator(operator)
        return assignment_to_json(AssignmentModel.get_assignments_by_operator(operator))
    
    # @staticmethod
    # def get_assignments_by_operator_pending(operator: str):
    #     """Get all assignments by operator and status assignment is 'PENDING'.
        
    #     Parameters
    #     ----------
    #     operator : str
    #         The operator's username.
    #     """
    #     AssignmentModel.get_assignments_by_operator_pending(operator)
    #     return assignment_to_json(AssignmentModel.get_assignments_by_operator_pending(operator))