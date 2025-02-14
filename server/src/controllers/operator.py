from datetime import datetime
from typing import List
from constants import AccountType, StatusAssignmentType
from models import Operator, OperatorModel, Assignment, AssignmentModel
from schemas import (
    OperatorSchema, 
    OperatorRegisterBody, 
    OperatorUpdateBody, 
    AssignmentSchema, 
    AssignmentRegisterBody, 
    AssignmentReassignBody,
    AssignmentsCountResponse
)
from utils import encrypt, Log, is_valid_account_type, is_valid_profile_type, is_valid_status_assignment_type


class OperatorController:

    # NOTE: OPERATION OF OPERATOR MODELS
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
                return []
            model = Operator()
            return model.get_all_profile_active(profile)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

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
                return False
            if OperatorController.get_operator(body.username):
                raise Exception("Username invalid")
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
                return False
            body.account = body.account.upper()
            if not is_valid_account_type(body.account):
                return False
            body.profile = body.profile.upper()
            if not is_valid_profile_type(body.profile):
                return False
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
                return False
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
                return False
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
                raise Exception("Operator not found")
            model = Assignment(
                id_change_interface=body.change_interface,
                id_old_interface=body.old_interface,
                operator=body.operator,
            )
            if model.get_assignment_by_interface():
                raise Exception("Interface already assigned")
            new_assignment = AssignmentModel(
                change_interface=body.change_interface,
                old_interface=body.old_interface,
                operator=body.operator,
                date_assignment=datetime.now().strftime("%Y-%m-%d"),
                status_assignment=StatusAssignmentType.PENDING.value,
                assigned_by=body.assigned_by,
            )
            return new_assignment.register()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False

    @staticmethod
    def get_assignment(id: int) -> AssignmentSchema | None:
        """Obtain an assignment object with all information of the assignment.

        Parameters
        ----------
        id : int
            ID of the assignment.
        """
        try:
            model = Assignment(id=id)
            return model.get_by_id()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None
        
    @staticmethod
    def get_total_assignments() -> AssignmentsCountResponse | None:
        """Obtain the total number of pending and revised assignments of the system."""
        try:
            pending = Assignment.get_count_all_pending()
            revised = Assignment.get_count_all_revised()
            return AssignmentsCountResponse(
                total_pending=pending,
                total_revised=revised
            )
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None
        
    @staticmethod
    def get_all_assignments_revised() -> List[AssignmentSchema]:
        """Obtain a list of all revised assignments in the system."""
        try:
            inspect = Assignment.get_all_by_status(StatusAssignmentType.INSPECTED.value)
            rediscovered = Assignment.get_all_by_status(StatusAssignmentType.REDISCOVERED.value)
            return inspect + rediscovered
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []
        
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
                raise Exception("Operator not found")
            model = Assignment(operator=operator)
            return model.get_all_by_operator()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    @staticmethod
    def get_all_assignments_pending_by_operator(operator: str) -> List[AssignmentSchema]:
        """Obtain a list of all pending assignments of an operator in the system.

        Parameters
        ----------
        operator : str
            Username of the operator.
        """
        try:
            if not OperatorController.get_operator(operator):
                raise Exception("Operator not found")
            model = Assignment(operator=operator)
            return model.get_all_status_by_operator(StatusAssignmentType.PENDING.value)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []
        
    @staticmethod
    def get_all_assignments_revised_by_operator(operator: str) -> List[AssignmentSchema]:
        """Obtain a list of all revised assignments of an operator in the system.

        Parameters
        ----------
        operator : str
            Username of the operator.
        """
        try:
            if not OperatorController.get_operator(operator):
                raise Exception("Operator not found")
            model = Assignment(operator=operator)
            inspect = model.get_all_status_by_operator(StatusAssignmentType.INSPECTED.value)
            rediscovered = model.get_all_status_by_operator(StatusAssignmentType.REDISCOVERED.value)
            return inspect + rediscovered
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []
        
    @staticmethod
    def get_total_assignments_by_operator(operator: str) -> AssignmentsCountResponse | None:
        """Obtain the total number of pending and revised assignments of an operator in the system.

        Parameters
        ----------
        operator : str
            Username of the operator.
        """
        try:
            if not OperatorController.get_operator(operator):
                raise Exception("Operator not found")
            model = Assignment(operator=operator)
            pending = model.get_count_pending_by_operator()
            revised = model.get_count_revised_by_operator()
            return AssignmentsCountResponse(
                total_pending=pending,
                total_revised=revised
            )
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None
        
    @staticmethod
    def reassignment(body: AssignmentReassignBody) -> bool:
        """Reassign an assignment in the system.

        Parameters
        ----------
        body : AssignmentReassignBody
            Data of the assignment to reassign.
        """
        try:
            if not OperatorController.get_operator(body.new_operator):
                raise Exception("Operator not found")
            model = Assignment(id=body.id_assignment)
            if not model.get_by_id():
                raise Exception("Assignment not found")
            return model.update_operator(body.new_operator, body.assigned_by)
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
                return False
            model = Assignment(id=id)
            if not model.get_by_id():
                return False
            return model.update_status(status)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False