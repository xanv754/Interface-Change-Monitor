from typing import Tuple, List
from datetime import datetime, timedelta
from pandas import DataFrame
from constants.header import HEADER_RESPONSE_INTERFACES_CHANGES
from constants.code import ResponseCode
from database.querys.assignment import AssignmentQuery
from database.querys.user import UserQuery
from models.assignment import NewAssignmentModel, AssignmentModel, ReassignmentModel, UpdateAssignmentModel
from utils.operation import OperationData
from utils.validate import Validate
from utils.log import log


class AssignmentController:
    """Class to manage assignment controller."""

    @staticmethod
    def new_assignment(assignments: List[NewAssignmentModel]) -> ResponseCode:
        """Insert a new assignment.
        
        Parameters
        ----------
        assignment : NewAssignmentModel
            Assignment to insert.
        """
        try:
            query = AssignmentQuery()
            buffer = OperationData.transform_to_buffer(assignments)
            status_operation = query.insert(data=buffer)
            if not status_operation: raise Exception()
            return ResponseCode(status=201)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment controller error. Failed to insert a new assignment. {error}")
            return ResponseCode(status=500)
        
    @staticmethod
    def reassign(assignments: List[ReassignmentModel]) -> ResponseCode:
        """Reassign assignments.
        
        Parameters
        ----------
        assignment : List[ReassignmentModel]
            Assignment to reassign.
        """
        try:
            query = AssignmentQuery()
            status_operation = query.reassing(data=assignments)
            if not status_operation: raise Exception()
            return ResponseCode(status=200)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment controller error. Failed to reassign assignments. {error}")
            return ResponseCode(status=500)
        
    @staticmethod
    def update_status_assignment(assignments: List[UpdateAssignmentModel]) -> ResponseCode:
        """Update assignments status.
        
        Parameters
        ----------
        assignment : List[UpdateAssignmentModel]
            Assignment to update status.
        """
        try:
            query = AssignmentQuery()
            status_operation = query.update_status(data=assignments)
            if not status_operation: raise Exception()
            return ResponseCode(status=200)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment controller error. Failed to update assignments status. {error}")
            return ResponseCode(status=500)
        
    @staticmethod
    def get_all_assignments_filter_by_status(status: str) -> Tuple[ResponseCode, List[dict]]:
        """Get all assignments filter by a status.
        
        Parameters
        ----------
        status : str
            Status to get assignments.

        Returns
        -------
        Tuple[ResponseCode, DataFrame]
            Response code and a list of assignments.
        """
        try:
            query = AssignmentQuery()
            if not Validate.assignment_status(status=status):
                return ResponseCode(status=400, message="Invalid status"), []
            data = query.get_all_by_status(status=status)
            if data.empty: return ResponseCode(status=200), []
            data = OperationData.transform_to_json(data=data)
            return ResponseCode(status=200), data
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment controller error. Failed to get assignments by status. {error}")
            return ResponseCode(status=500), []
        
    @staticmethod
    def get_user_assignments_filter_by_status(username: str, status: str) -> Tuple[ResponseCode, List[dict]]:
        """Get user assignments filter by a status.
        
        Parameters
        ----------
        username : str
            Username to get assignments.
        status : str
            Status to get assignments.

        Returns
        -------
        Tuple[ResponseCode, DataFrame]
            Response code and a list of assignments.
        """
        try:
            if not Validate.assignment_status(status=status):
                return ResponseCode(status=400, message="Invalid status"), []
            user_query = UserQuery()
            if not user_query.get(username=username):
                return ResponseCode(status=404, message="User not found"), []
            query = AssignmentQuery()
            data = query.assigned_by_status(username=username, status=status)
            if data.empty: return ResponseCode(status=200), []
            data = OperationData.transform_to_json(data=data)
            return ResponseCode(status=200), data
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment controller error. Failed to get assignments by username and status. {error}")
            return ResponseCode(status=500), []
        
    @staticmethod
    def get_user_assignments_completed_in_month(username: str, month: int) -> Tuple[ResponseCode, List[dict]]:
        """Get user assignments completed in a month.
        
        Parameters
        ----------
        username : str
            Username to get assignments.
        month : int
            Month to get assignments.

        Returns
        -------
        Tuple[ResponseCode, DataFrame]
            Response code and a list of assignments.
        """
        try:
            user_query = UserQuery()
            if not user_query.get(username=username):
                return ResponseCode(status=404, message="User not found"), []
            query = AssignmentQuery()
            data = query.completed_by_month(username=username, month=month)
            if data.empty: return ResponseCode(status=200), []
            data = OperationData.transform_to_json(data=data)
            return ResponseCode(status=200), data
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment controller error. Failed to get assignments completed in month. {error}")
            return ResponseCode(status=500), []
        
    @staticmethod
    def get_statistics_assignments(usernames: List[str]) -> Tuple[ResponseCode, List[dict]]:
        """Get statistics of assignments.
        
        Parameters
        ----------
        usernames : List[str]
            Usernames to get statistics.

        Returns
        -------
        Tuple[ResponseCode, DataFrame]
            Response code and a list of statistics.
        """
        try:
            query = AssignmentQuery()
            data = query.get_statistics(usernames=usernames)
            if not data: return ResponseCode(status=200), []
            data = OperationData.transform_to_json(data=data)
            return ResponseCode(status=200), data
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment controller error. Failed to get statistics. {error}")
            return ResponseCode(status=500), []