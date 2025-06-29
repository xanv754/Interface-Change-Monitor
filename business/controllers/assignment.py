import pandas as pd
from typing import Tuple, List
from access.querys.assignment import AssignmentQuery
from access.querys.change import ChangeQuery
from access.querys.user import UserQuery
from access.models.assignment import UpdateAssignmentModel as AssignmentModel
from business.constants.header import HEADER_AUTOMATIC_ASSIGNMENT
from business.libs.code import ResponseCode
from business.models.assignment import NewAssignmentModel, ReassignmentModel, UpdateAssignmentModel
from business.models.change import UpdateChangeModel
from constants.fields import AssignmentField, ChangeAssignField
from constants.types import AssignmentStatusTypes
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
            assignment_query = AssignmentQuery()
            buffer = OperationData.transform_to_buffer(assignments)
            status_operation = assignment_query.insert(data=buffer)
            if not status_operation: raise Exception()
            changes: List[UpdateChangeModel] = []
            for assignment in assignments:
                changes.append(
                    UpdateChangeModel(
                        id_old=assignment.old_interface_id,
                        id_new=assignment.current_interface_id,
                        username=assignment.username
                    )
                )
            change_query = ChangeQuery()
            status_operation = change_query.update_assign(data=changes)
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
            changes: List[UpdateChangeModel] = []
            for assignment in assignments:
                changes.append(
                    UpdateChangeModel(
                        id_old=assignment.old_interface_id,
                        id_new=assignment.current_interface_id,
                        username=assignment.new_username
                    )
                )
            change_query = ChangeQuery()
            status_operation = change_query.update_assign(data=changes)
            if not status_operation: raise Exception()
            return ResponseCode(status=200)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment controller error. Failed to reassign assignments. {error}")
            return ResponseCode(status=500)
        
    @staticmethod
    def automatic_assignment(assign_by: str) -> ResponseCode:
        """Automatic assignment."""
        try:
            change_query = ChangeQuery()
            user_query = UserQuery()
            assign_query = AssignmentQuery()
            changes = change_query.get_all()
            if changes.empty: return ResponseCode(status=404, message="No change interfaces found")
            users = user_query.get_all()
            if not users: return ResponseCode(status=404, message="No users found")
            usernames = [user.username for user in users]
            total_users = len(users)
            total_changes = len(changes)
            base = total_changes // total_users
            rest = total_changes % total_users
            new_assignments = pd.DataFrame(columns=HEADER_AUTOMATIC_ASSIGNMENT)
            new_assignments[AssignmentField.OLD_INTERFACE_ID] = changes[ChangeAssignField.ID_OLD]
            new_assignments[AssignmentField.CURRENT_INTERFACE_ID] = changes[ChangeAssignField.ID_NEW]
            new_assignments[AssignmentField.USERNAME] = ""
            new_assignments[AssignmentField.ASSIGN_BY] = assign_by
            new_assignments[AssignmentField.TYPE_STATUS] = AssignmentStatusTypes.PENDING
            start = 0
            for i, username in enumerate(usernames):
                count = base + (1 if i < rest else 0)
                end = start + count
                new_assignments.loc[start: end - 1, AssignmentField.USERNAME] = username
                start = end
            buffer = OperationData.transform_to_buffer(new_assignments)
            status_operation = assign_query.insert(data=buffer)
            if not status_operation: raise Exception()
            changes: List[UpdateChangeModel] = []
            for _index, row in new_assignments.iterrows():
                changes.append(
                    UpdateChangeModel(
                        id_old=row[AssignmentField.OLD_INTERFACE_ID],
                        id_new=row[AssignmentField.CURRENT_INTERFACE_ID],
                        username=row[AssignmentField.USERNAME]
                    )
                )
            change_query = ChangeQuery()
            status_operation = change_query.update_assign(data=changes)
            if not status_operation: raise Exception()
            return ResponseCode(status=201)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Assignment controller error. Failed to automatic assignment. {error}")
            return ResponseCode(status=500)
        
    @staticmethod
    def update_status_assignment(assignments: List[UpdateAssignmentModel], username: str) -> ResponseCode:
        """Update assignments status.
        
        Parameters
        ----------
        assignment : List[UpdateAssignmentModel]
            Assignment to update status.
        """
        try:
            query = AssignmentQuery()
            list_assingments: AssignmentModel = []
            for assignment in assignments:
                list_assingments.append(
                    AssignmentModel(
                        old_interface_id=assignment.old_interface_id,
                        current_interface_id=assignment.current_interface_id,
                        username=username,
                        type_status=assignment.type_status
                    )
                )
            status_operation = query.update_status(data=list_assingments)
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
        Tuple[ResponseCode, List[dict]]
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
    def get_users_assignments_completed_in_month(usernames: List[str], month: int) -> Tuple[ResponseCode, List[dict]]:
        """Get assignments completed in a month of all users.
        
        Parameters
        ----------
        usernames : List[str]
            Usernames to get assignments.
        month : int
            Month to get assignments.

        Returns
        -------
        Tuple[ResponseCode, List[dict]]
            Response code and a list of assignments.
        """
        try:
            response = []
            for username in usernames:
                user_query = UserQuery()
                if not user_query.get(username=username): continue
                query = AssignmentQuery()
                data = query.completed_by_month(username=username, month=month)
                if data.empty: continue
                data = OperationData.transform_to_json(data=data)
                if not response: response = data
                else: response = response + data
            return ResponseCode(status=200), response
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