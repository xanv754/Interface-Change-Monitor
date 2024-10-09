from querys.member.find import find_type_user, find_user
from constants.assigmentStatus import assignmentstatus
from querys.member.delete import delete_users_disabled
from controllers.element import ElementController
from querys.member.update import update_assigned
from models.assignment import AssignmentModel
from models.interface import InterfaceModel
from constants.userStatus import userstatus
from entity.user import User
from typing import List

class User_Controller():
    def read_users(self) -> List[User]:
        try:
            return find_type_user()
        except Exception as error:
            print(error)
            return None
        
    def read_user(self, username: str) -> User:
        try:
            user: User = find_user(username)
            return user
        except Exception as error:
            print(error)
            return None

    def update_assigned(self, assigned_username: str, assigned_element_id: str, new_assignment: AssignmentModel) -> bool:
        try:
            user = self.read_user(assigned_username)
            if user and user.status == userstatus.enabled:
                res = ElementController.update_assignment(assigned_element_id, new_assignment)
                if res:
                    assigned_interface = ElementController.read_interface_element(assigned_element_id)
                    assignments = user.assigned
                    if new_assignment.status == assignmentstatus.pending:
                        assignments.append(assigned_interface)
                        update_assigned(assigned_username, assignments)
                    elif new_assignment.status != assignmentstatus.default:
                        for assigned in assignments:
                            if assigned.idElement == assigned_element_id:
                                assignments.remove(assigned)
                                assignments.append(assigned_interface)
                                update_assigned(assigned_username, assignments)
                                break
                return res
            else: return False
        except Exception as error:
            print(error)
            return False
        
    def clean_users_disabled(self) -> bool:
        try:
            res = delete_users_disabled()
            if res: return res.acknowledged
            return False
        except Exception as error:
            print(error)
            return False
        
    def clean_assigned(self, username: str, assigned: List[InterfaceModel]) -> bool:
        try:
            res = update_assigned(username, assigned)
            if res: return res.acknowledged
            return False
        except Exception as error:
            print(error)
            return False
        
UserController = User_Controller()