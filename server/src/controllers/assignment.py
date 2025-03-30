import random
from typing import List
from controllers.change import ChangeController
from controllers.operator import OperatorController
from database.models.assignment import AssignmentModel, AssignmentInfoModel, AssignmentStatisticsModel
from schemas.assignment import (
    AssignmentSchema,
    ReassignBody,
    RegisterAssignmentBody,
    RegisterAutoAssignment,
    AssignmentInterfaceSchema,
    AssignmentInterfaceAssignedSchema,
    UpdateStatusAssignmentBody,
    AssignmentStatisticsSchema,
    AssignmentStatisticsOperatorSchema
)
from utils.valid import ValidDataHandler
from utils.log import LogHandler


class AssignmentController:
    """Controller for all operations of assignment table."""

    @staticmethod
    def add_assignment(body: List[RegisterAssignmentBody]) -> bool:
        """Register a new assignments.

        Parameters
        ----------
        body : List[RegisterAssignmentBody]
            List of new assignments.
        """
        try:
            if (body):
                operator = body[0].operator
                if not OperatorController.get_operator(operator):
                    raise Exception("Failed to update operator. Operator not found")
                status_assignment = AssignmentModel.register(body)
                if status_assignment:
                    ids = [x.idChange for x in body]
                    return ChangeController.update_operator(ids, operator)
                else:
                    raise Exception("Failed to register new assignments. Some assignments not registered")
            else:
                return True
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False

    @staticmethod
    def reassignment(body: List[ReassignBody]) -> bool:
        """Reassign an assignment in the system.

        Parameters
        ----------
        body : ReassignBody
            Data of the assignment to reassign.
        """
        try:
            if (body):
                new_operator = body[0].newOperator
                if not OperatorController.get_operator(new_operator):
                    raise Exception("Failed to reassign an assignment. Operator not found")
                status = AssignmentModel.reassing(body)
                if status:
                    ids = [x.idAssignment for x in body]
                    return ChangeController.update_operator(ids, new_operator)
                else:
                    raise Exception("Failed to reassign an assignment. Some assignments not reassigned")
            else:
                return True
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False

    @staticmethod
    def auto_assignment(body: RegisterAutoAssignment) -> bool:
        """Auto assign all changes of the system.

        Parameters
        ----------
        body : RegisterAutoAssignment
            Data of the auto assignment.
        """
        try:
            changes = ChangeController.get_all_changes()
            changes = [change for change in changes if change.operator == None]
            if (changes):
                total_changes = len(changes)
                total_users = len(body.users)
                partition_general = total_changes // total_users
                partition_special = total_changes % total_users
                for username in body.users:
                    data: List[RegisterAssignmentBody] = []
                    changes_user = changes[0:partition_general + 1]
                    for change in changes_user:
                        new_data = RegisterAssignmentBody(
                            idChange=change.id,
                            newInterface=change.newInterface.id,
                            oldInterface=change.oldInterface.id,
                            operator=username,
                            assignedBy=body.assignedBy
                        )
                        data.append(new_data)
                    status = AssignmentController.add_assignment(data)
                    if not status:
                        raise Exception(f"Some auto assignments not registered by the user {username}")
                    changes = changes[partition_general + 1:]
                if (partition_special > 0):
                    username = random.choice(body.users)
                    data: List[RegisterAssignmentBody] = []
                    for change in changes:
                        new_data = RegisterAssignmentBody(
                            idChange=change.id,
                            newInterface=change.newInterface.id,
                            oldInterface=change.oldInterface.id,
                            operator=username,
                            assignedBy=body.assignedBy
                        )
                        data.append(new_data)
                    status = AssignmentController.add_assignment(data)
                    if not status:
                        raise Exception(f"Some auto assignments not registered by the user {username}")
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
        else:
            return True

    @staticmethod
    def get_assignment_by_id(id: int) -> AssignmentSchema | None:
        """Obtain an assignment by your ID.

        Parameters
        ----------
        id : int
            ID of the assignment.
        """
        try:
            return AssignmentModel.get_by_id(id=id)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_info_assignment_by_id(id: int) -> AssignmentInterfaceSchema | None:
        """Obtain assignment with all information (interfaces, operator, etc.) by your ID.

        Parameters
        ----------
        id : int
            ID of the assignment.
        """
        try:
            return AssignmentInfoModel.get_by_id(id=id)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_all_assignments_by_operator(operator: str) -> List[AssignmentSchema]:
        """Obtain a list of all assignments (pending and revised) of an operator.

        Parameters
        ----------
        operator : str
            Username of the operator.
        """
        try:
            if not OperatorController.get_operator(operator):
                raise Exception("Failed to get all assignments of an operator. Operator not found")
            return AssignmentModel.get_by_operator(username=operator)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_all_pending_assignments_by_operator(operator: str) -> List[AssignmentInterfaceSchema]:
        """Obtain a list of all info pending assignments of an operator.

        Parameters
        ----------
        operator : str
            Username of the operator.
        """
        try:
            if not OperatorController.get_operator(operator):
                raise Exception("Failed to get all assignments of an operator. Operator not found")
            return AssignmentInfoModel.get_pending(username=operator)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_all_revised_assignments_by_operator(operator: str) -> List[AssignmentInterfaceSchema]:
        """Obtain a list of all info assignments (revised) of an operator in the system.

        Parameters
        ----------
        operator : str
            Username of the operator.
        """
        try:
            if not OperatorController.get_operator(operator):
                raise Exception("Failed to get all assignments of an operator. Operator not found")
            return AssignmentInfoModel.get_revised(username=operator)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_all_revised_assignments_by_month(month: int) -> List[AssignmentInterfaceAssignedSchema]:
        """Obtain a list of all info assignments (revised) in the system by a month.

        Parameters
        ----------
        month : int
            Month to get the assignments revised.
        """
        try:
            return AssignmentInfoModel.get_revised_by_month(month=month)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_statistics_general_by_day(day: str) -> AssignmentStatisticsSchema | None:
        """Obtain the total number of pending and revised assignments of the system.

        Parameters
        -----------
        day : str
            Day to get the statistics.
        """
        try:
            return AssignmentStatisticsModel.get_general_by_day(day=day)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_statistics_general_by_month(month: int) -> AssignmentStatisticsSchema | None:
        """Obtain the total number of pending and revised assignments of the system.

        Parameters
        -----------
        day : str
            Day to get the statistics.
        """
        try:
            return AssignmentStatisticsModel.get_general_by_month(month=month)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_statistics_general_operators() -> List[AssignmentStatisticsOperatorSchema]:
        """Obtain the total number of pending and revised assignments of the system by each operator."""
        try:
            return AssignmentStatisticsModel.get_general_by_operators()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_statistics_general_operators_by_day(day: str) -> List[AssignmentStatisticsOperatorSchema]:
        """Obtain the total number of pending and revised assignments of the system.

        Parameters
        -----------
        day : str
            Day to get the statistics.
        """
        try:
            return AssignmentStatisticsModel.get_general_operators_by_day(day=day)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_statistics_general_operators_by_month(month: int) -> List[AssignmentStatisticsOperatorSchema]:
        """Obtain the total number of pending and revised assignments of the system.

        Parameters
        -----------
        day : str
            Day to get the statistics.
        """
        try:
            return AssignmentStatisticsModel.get_general_operators_by_month(month=month)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return []

    @staticmethod
    def get_statistics_assignments_operator(operator: str) -> AssignmentStatisticsOperatorSchema | None:
        """Obtain the total number of pending and revised assignments of an operator in the system.

        Parameters
        -----------
        operator : str
            The username of the operator.
        """
        try:
            return AssignmentStatisticsModel.get_operator(username=operator)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_statistics_assignments_operator_by_day(operator: str, day: str) -> AssignmentStatisticsOperatorSchema | None:
        """Obtain the total number of pending and revised assignments of an operator in the system.

        Parameters
        -----------
        operator : str
            The username of the operator.
        day : str
            Day to get the statistics.
        """
        try:
            return AssignmentStatisticsModel.get_operator_by_day(username=operator, day=day)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def get_statistics_assignments_operator_by_month(operator: str, month: int) -> AssignmentStatisticsOperatorSchema | None:
        """Obtain the total number of pending and revised assignments of an operator in the system.

        Parameters
        -----------
        operator : str
            The username of the operator.
        month : int
            Month to get the statistics.
        """
        try:
            return AssignmentStatisticsModel.get_operator_by_month(username=operator, month=month)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return None

    @staticmethod
    def update_status_assignment(id: int, status: str) -> bool:
        """Update status of an assignment in the system.

        Parameters
        ----------
        id : int
            ID of the assignment.
        status : str
            New status of the assignment.
            - **PENDING:** Pending assignment.
            - **INSPECTED:** Inspected assignment.
            - **REDISCOVERED:** Rediscovered assignment.
        """
        try:
            status = status.upper()
            if not ValidDataHandler.status_assignment_type(status):
                raise Exception("Failed to update status assignment. Invalid status assignment type")
            if not AssignmentController.get_assignment_by_id(id):
                raise Exception("Failed to update status assignment. Assignment not found")
            return AssignmentModel.update_status_by_id(id=id, status=status)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False

    @staticmethod
    def update_status_assignments_by_ids(data: List[UpdateStatusAssignmentBody]) -> bool:
        """Update status of many assignments in the system.

        Parameters
        ----------
        data : List[AssignmentUpdateStatus]
            List of assignments to update.
        """
        try:
            status = data[0].newStatus
            if not ValidDataHandler.status_assignment_type(status):
                raise Exception("Failed to update status assignment. Invalid status assignment type")
            ids: List[int] = [x.idAssignment for x in data]
            return AssignmentModel.update_status(ids, status)
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            return False
