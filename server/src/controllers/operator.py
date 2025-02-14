from datetime import datetime
from typing import List
from constants import AccountType, StatusAssignmentType
from models import Operator, OperatorModel, Assignment, AssignmentModel
from schemas import OperatorSchema, OperatorRegisterBody, OperatorUpdateBody, AssignmentSchema, AssignmentRegisterBody
from utils import encrypt, Log, is_valid_account_type, is_valid_profile_type, is_valid_status_assignment_type


class OperatorController:
    @staticmethod
    def get_operator(username: str, confidential: bool = True) -> OperatorSchema | None:
        try:
            model = Operator(username=username)
            return model.get(confidential=confidential)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    @staticmethod
    def register_operator(body: OperatorRegisterBody) -> bool:
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
    def add_assignment(body: AssignmentRegisterBody) -> bool:
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
        try:
            model = Assignment(id=id)
            return model.get_by_id()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return None

    @staticmethod
    def get_assignments_pending(operator: str) -> List[AssignmentSchema]:
        try:
            if not OperatorController.get_operator(operator):
                raise Exception("Operator not found")
            model = Assignment(operator=operator)
            return model.get_all_by_status(StatusAssignmentType.PENDING.value)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    @staticmethod
    def get_all_assignments(operator: str) -> List[AssignmentSchema]:
        try:
            if not OperatorController.get_operator(operator):
                raise Exception("Operator not found")
            model = Assignment(operator=operator)
            return model.get_all_by_operator()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return []

    @staticmethod
    def update_status_assignment(id: int, status: str) -> bool:
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

    @staticmethod
    def update_operator(body: OperatorUpdateBody) -> bool:
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
        try:
            operator = Operator(username=username)
            if not operator.get():
                return False
            password_hash = encrypt.get_password_hash(password)
            return operator.update_password(password_hash)
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False
