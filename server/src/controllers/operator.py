import random
from typing import List
from constants import AccountType, StatusAssignmentType
from controllers.change import ChangeController
from database import Operator, OperatorModel, Assignment, AssignmentModel
from schemas import (
    OperatorSchema,
    RegisterUserBody,
    UpdateUserRootBody,
    AssignmentSchema,
    UpdateStatusAssignmentBody,
    RegisterAssignmentBody,
    ReassignBody,
    AssignmentStatisticsOperatorSchema,
    AssignmentStatisticsSchema,
    AssignmentInterfaceSchema,
    AssignmentInterfaceAssignedSchema,
    RegisterAutoAssignment
)
from utils import encrypt, Log, is_valid_account_type, is_valid_profile_type, is_valid_status_assignment_type


class OperatorController:

    # NOTE: OPERATION OF OPERATOR MODELS
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
            if not is_valid_profile_type(body.profile):
                raise Exception("Failed to register operator. Invalid profile type")
            if OperatorController.get_operator(body.username):
                raise Exception("Failed to register operator. Username not available")
            password_hash = encrypt.get_password_hash(body.password)
            new_operator = OperatorModel(
                username=body.username,
                name=body.name,
                lastname=body.lastname,
                password=password_hash,
                profile=body.profile,
                statusaccount=AccountType.ACTIVE.value,
            )
            return new_operator.register()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False

    @staticmethod
    def get_operator(username: str, confidential: bool = True) -> OperatorSchema | None:
        """Obtain an operator object with all information of the operator.

        Parameters
        ----------
        confidential: bool
            If True, the password is not returned.
        """
        try:
            model = Operator(username=username)
            return model.get(confidential=confidential)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    @staticmethod
    def get_operators() -> List[OperatorSchema]:
        """Obtain a list of all operators (except those to be deleted) in the system."""
        try:
            return Operator.get_all_without_deleted()
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            if not is_valid_profile_type(profile):
                raise Exception("Failed to get operators profile active. Invalid profile type")
            return Operator.get_all_profile_active(profile)
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            operator = Operator(username=body.username)
            if not operator.get():
                raise Exception("Failed to update operator. Operator not found")
            body.account = body.account.upper()
            if not is_valid_account_type(body.account):
                raise Exception("Failed to update operator. Invalid account type")
            body.profile = body.profile.upper()
            if not is_valid_profile_type(body.profile):
                raise Exception("Failed to update operator. Invalid profile type")
            model = OperatorModel(
                username=body.username,
                name=body.name,
                lastname=body.lastname,
                password="",
                profile=body.profile,
                statusaccount=body.account,
            )
            return model.update()
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            operator = Operator(username=username)
            if not operator.get():
                raise Exception("Failed to update password of an operator. Operator not found")
            password_hash = encrypt.get_password_hash(password)
            return operator.update_password(password_hash)
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            operator = Operator(username=username).get()
            if not operator:
                raise Exception("Failed to delete operator. Operator not found")
            model = OperatorModel(
                username=operator.username,
                name=operator.name,
                lastname=operator.lastname,
                password="",
                profile=operator.profile,
                statusaccount=AccountType.DELETED.value,
            )
            return model.update()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False


    # NOTE: OPERATION OF ASSIGNMENT MODELS
    @staticmethod
    def add_assignment(body: List[RegisterAssignmentBody]) -> bool:
        """Register a new assignment in the system.

        Parameters
        ----------
        body : RegisterAssignmentBody
            Data of the new assignment.
        """
        try:
            if (body):
                new_operator = body[0].operator
                if not OperatorController.get_operator(new_operator):
                    raise Exception("Failed to update operator. Operator not found")
                model = AssignmentModel()
                status_assignment = model.register(body)
                if status_assignment:
                    ids = [x.idChange for x in body]
                    return ChangeController.update_operator(ids, new_operator)
                else:
                    raise Exception("Failed to register new assignments. Some assignments not registered")
            else:
                return True
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
                model = AssignmentModel()
                status = model.reassing(body)
                if status:
                    ids = [x.idAssignment for x in body]
                    return ChangeController.update_operator(ids, new_operator)
                else:
                    raise Exception("Failed to reassign an assignment. Some assignments not reassigned")
            else:
                return True
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
                    status = OperatorController.add_assignment(data)
                    if not status:
                        raise Exception(f"Some auto assignments not registered by the user {username}")
                    changes = changes[partition_general + 1:]
                if (partition_special > 0):
                    username = random.choice(body.users)
                    data: List[RegisterAssignmentBody] = []
                    for change in changes:
                        new_data = RegisterAssignmentBody(
                            idChange=change.id,
                            newInterface=change.newInterface,
                            oldInterface=change.oldInterface,
                            operator=username,
                            assignedBy=body.assignedBy
                        )
                        data.append(new_data)
                    status = OperatorController.add_assignment(data)
                    if not status:
                        raise Exception(f"Some auto assignments not registered by the user {username}")
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            model = Assignment(id=id)
            return model.get_assignment_by_id_assignment()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    @staticmethod
    def get_info_assignment_by_id(id: int) -> AssignmentInterfaceSchema:
        """Obtain assignment with all information (interfaces, operator, etc.) by your ID.

        Parameters
        ----------
        id : int
            ID of the assignment.
        """
        try:
            model = Assignment(id=id)
            return model.get_info_assignment_by_id_assignment()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    @staticmethod
    def get_all_assignments_by_operator(operator: str) -> List[AssignmentSchema]:
        """Obtain a list of all assignments (pending and revised) of an operator in the system.

        Parameters
        ----------
        operator : str
            Username of the operator.
        """
        try:
            if not OperatorController.get_operator(operator):
                raise Exception("Failed to get all assignments of an operator. Operator not found")
            model = Assignment(operator=operator)
            return model.get_all_assignments_by_operator()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    @staticmethod
    def get_all_pending_assignments_by_operator(operator: str) -> List[AssignmentInterfaceSchema]:
        """Obtain a list of all info assignments (pending) of an operator in the system.

        Parameters
        ----------
        operator : str
            Username of the operator.
        """
        try:
            if not OperatorController.get_operator(operator):
                raise Exception("Failed to get all assignments of an operator. Operator not found")
            model = Assignment(operator=operator)
            return model.get_all_info_assignments_pending_by_operator()
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            model = Assignment(operator=operator)
            return model.get_all_info_assignments_revised_by_operator()
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            return Assignment.get_all_info_assignments_revised_by_month(month=month)
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            return Assignment.get_statistics_general_by_day(day=day)
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            return Assignment.get_statistics_general_by_month(month=month)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    @staticmethod
    def get_statistics_general_operators() -> List[AssignmentStatisticsOperatorSchema]:
        """Obtain the total number of pending and revised assignments of the system by each operator."""
        try:
            return Assignment.get_statistics_assignments_general()
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            return Assignment.get_statistics_assignments_general_by_day(day=day)
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            return Assignment.get_statistics_assignments_general_by_month(month=month)
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            model = Assignment(operator=operator)
            return model.get_statistics_assignments_operator()
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            model = Assignment(operator=operator)
            return model.get_statistics_assingments_operator_by_day(day=day)
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            model = Assignment(operator=operator)
            return model.get_statistics_assingments_operator_by_month(month=month)
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            if not is_valid_status_assignment_type(status):
                raise Exception("Failed to update status assignment. Invalid status assignment type")
            model = Assignment(id=id)
            if not model.get_assignment_by_id_assignment():
                raise Exception("Failed to update status assignment. Assignment not found")
            return model.update_status(status)
        except Exception as e:
            Log.save(e, __file__, Log.error)
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
            if not is_valid_status_assignment_type(status):
                raise Exception("Failed to update status assignment. Invalid status assignment type")
            ids: List[int] = [x.idAssignment for x in data]
            return Assignment.update_status_by_ids(ids, status)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False
