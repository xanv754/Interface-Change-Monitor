from datetime import datetime
from typing import List
from constants import AccountType, StatusAssignmentType
from models import (
    Operator, 
    OperatorModel, 
    OperatorRegisterBody,
    Assignment,
    AssignmentModel,
    AssignmentRegisterRequest
)


class OperatorController:
    @staticmethod
    def get_operator(username: str) -> dict | None:
        try:
            model = Operator(username=username)
            return model.get()
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def register(body: OperatorRegisterBody) -> bool:
        try:
            if OperatorController.get_operator(body.username): raise Exception("Username already exists")
            # TODO: Hash the password
            new_operator = OperatorModel(
                username=body.username,
                name=body.name,
                lastname=body.lastname,
                password=body.password,
                profile=body.profile,
                statusaccount=AccountType.ACTIVE.value,
            )
            return new_operator.register()
        except Exception as e:
            print(e)
            return False
        
    @staticmethod
    def new_assignment(body: AssignmentRegisterRequest) -> bool:
        try:
            if not OperatorController.get_operator(body.operator): raise Exception("Operator not found")
            model = Assignment(
                id_change_interface=body.change_interface,
                id_old_interface=body.old_interface,
                operator=body.operator,
            )
            if model.get_assignment_by_interface(): raise Exception("Interface already assigned")
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
            print(e)
            return False
        
    @staticmethod
    def get_assignments(operator: str) -> List[dict]:
        try:
            if not OperatorController.get_operator(operator): raise Exception("Operator not found")
            model = Assignment(operator=operator)
            return model.get_all_by_status(StatusAssignmentType.PENDING.value)
        except Exception as e:
            print(e)
            return []
        
    @staticmethod
    def get_all_assignments(operator: str) -> List[dict]:
        try:
            if not OperatorController.get_operator(operator): raise Exception("Operator not found")
            model = Assignment(operator=operator)
            return model.get_all_by_operator()
        except Exception as e:
            print(e)
            return []