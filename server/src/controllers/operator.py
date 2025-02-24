from datetime import datetime
from typing import List
from constants import AccountType, StatusAssignmentType
from models import Operator, OperatorModel, Assignment, AssignmentModel
from schemas import (
    OperatorResponseSchema,
    OperatorResponse,
    OperatorRegisterBody,
    OperatorUpdateBody,
    AssignmentResponseSchema,
    AssignmentUpdateStatus,
    AssignmentRegisterBody,
    AssignmentReassignBody,
    AssignmentStatisticsResponse,
    AssignmentInterfaceResponseSchema
)
from utils import encrypt, Log, is_valid_account_type, is_valid_profile_type, is_valid_status_assignment_type


class OperatorController:

    # NOTE: OPERATION OF OPERATOR MODELS
    @staticmethod
    def register_operator(body: OperatorRegisterBody) -> bool:
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
    def get_operator(username: str, confidential: bool = True) -> OperatorResponseSchema | None:
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
    def get_operators() -> List[OperatorResponseSchema]:
        """Obtain a list of all operators (except those to be deleted) in the system."""
        try:
            return Operator.get_all_without_deleted()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    @staticmethod
    def get_operators_profile_active(profile: str) -> List[OperatorResponseSchema]:
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
    def update_operator(body: OperatorUpdateBody) -> bool:
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
    def add_assignment(body: AssignmentRegisterBody) -> bool:
        """Register a new assignment in the system.

        Parameters
        ----------
        body : AssignmentRegisterBody
            Data of the new assignment.
        """
        try:
            if not OperatorController.get_operator(body.operator):
                raise Exception("Failed to update operator. Operator not found")
            model = Assignment(
                id_new_interface=body.newInterface,
                id_old_interface=body.oldInterface,
                operator=body.operator,
            )
            if model.get_assignment_by_interface():
                Log.save("Failed to register new assignment. Interface already assigned", __file__, Log.warning)
                return True
            new_assignment = AssignmentModel(
                new_interface=body.newInterface,
                old_interface=body.oldInterface,
                operator=body.operator,
                date_assignment=datetime.now().strftime("%Y-%m-%d"),
                status_assignment=StatusAssignmentType.PENDING.value,
                assigned_by=body.assignedBy,
            )
            return new_assignment.register()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False

    @staticmethod
    def get_assignment_by_id(id: int) -> AssignmentResponseSchema | None:
        """Obtain an assignment by your ID.

        Parameters
        ----------
        id : int
            ID of the assignment.
        """
        try:
            model = Assignment(id=id)
            return model.get_by_id_assignment()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    @staticmethod
    def get_info_assignment_by_id(id: int) -> AssignmentInterfaceResponseSchema:
        """Obtain assignment with all information (interfaces, operator, etc.) by your ID.

        Parameters
        ----------
        id : int
            ID of the assignment.
        """
        try:
            model = Assignment(id=id)
            return model.get_info_assignment_by_id()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    @staticmethod
    def get_general_statistics_assignments() -> List[AssignmentStatisticsResponse]:
        """Obtain the total number of pending and revised assignments of the system."""
        try:
            return Assignment.get_all_statistics_assingments()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []
        
    @staticmethod
    def get_statistics_assignments_by_operator(operator: str) -> AssignmentStatisticsResponse | None:
        """Obtain the total number of pending and revised assignments of an operator in the system."""
        try:
            model = Assignment(operator=operator)
            return model.get_all_statistics_assingments_by_operator()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    @staticmethod
    def get_all_assignments_by_operator(operator: str) -> List[AssignmentResponseSchema]:
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
    def reassignment(body: AssignmentReassignBody) -> bool:
        """Reassign an assignment in the system.

        Parameters
        ----------
        body : AssignmentReassignBody
            Data of the assignment to reassign.
        """
        try:
            if not OperatorController.get_operator(body.newOperator):
                raise Exception("Failed to reassign an assignment. Operator not found")
            model = Assignment(id=body.idAssignment)
            if not model.get_by_id_assignment():
                raise Exception("Failed to reassign an assignment. Assignment not found")
            return model.update_operator(body.newOperator, body.assignedBy)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False

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
            if not model.get_by_id_assignment():
                raise Exception("Failed to update status assignment. Assignment not found")
            return model.update_status(status)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False

    @staticmethod
    def update_status_assignments_by_ids(data: List[AssignmentUpdateStatus]) -> bool:
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
