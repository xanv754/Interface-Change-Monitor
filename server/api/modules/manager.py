from utils.date import get_date, get_day, get_month, get_year
from constants.assigmentStatus import assignmentstatus
from controllers.element import ElementController
from controllers.admin import AdminController
from models.assignment import AssignmentModel
from modules.security import secure_password
from controllers.user import UserController
from constants.userStatus import userstatus
from models.register import RegisterModel
from constants.userType import usertype
from typing import List

class ManagerResponse:
    def create_new_user(self, new_user: RegisterModel):
        try:
            new_user.password = secure_password(new_user.password)
            user = AdminController.search_user(new_user.username)
            if user: return 2
            if new_user.type == usertype.admin:
                user = AdminController.new_admin(new_user)
                res = AdminController.create_admin(user)
                if res: return 1
                else: return 0
            else:
                user = AdminController.new_user(new_user)
                res = AdminController.create_user(user)
                if res: return 1
                else: return 0
        except Exception as error:
            print(error)
            return None
        
    def get_elements_backup(self):
        try:
            data = []
            res = ElementController.read_elements_backup()
            if res: 
                for a in res: data.append(a.model_dump())
            return data
        except Exception as error:
            print(error)
            return []
        
    def get_elements(self):
        try:
            data = []
            res = ElementController.read_elements()
            if res: 
                for a in res: data.append(a.model_dump())
            return data
        except Exception as error:
            print(error)
            return []
        
    def get_element(self, id: str):
        try:
            res = ElementController.read_element(id)
            if res: return res.model_dump()
            else: return None
        except Exception as error:
            print(error)
            return None
        
    def get_type_users(self):
        try:
            data = []
            res = UserController.read_users()
            if res: 
                for a in res: data.append(a.model_dump(exclude={'password'}))
            return data
        except Exception as error:
            print(error)
            return []
        
    def get_type_admin(self):
        try:
            data = []
            res = AdminController.read_users()
            if res: 
                for a in res: data.append(a.model_dump(exclude={'password'}))
            return data
        except Exception as error:
            print(error)
            return []
        
    def get_users(self):
        try:
            return AdminController.read_all_users()
        except Exception as error:
            print(error)
            return None
        
    def get_user(self, username: str):
        try:
            res = UserController.read_user(username)
            if res: return res.model_dump(exclude={'password'})
            else: return None
        except Exception as error:
            print(error)
            return None
        
    def get_admin(self, username: str):
        try:
            res = AdminController.read_admin(username)
            if res: return res.model_dump(exclude={'password'})
            else: return None
        except Exception as error:
            print(error)
            return None
        
    def get_users_pending(self):
        try:
            return AdminController.read_users_pending()
        except Exception as error:
            print(error)
            return []
        
    def update_status_user(self, username: str, status: str):
        try:
            if status == userstatus.enabled:
                return AdminController.accept_user(username)
            else: return AdminController.delete_user(username)
        except Exception as error:
            print(error)
            return None
        
    def update_assign_element(self, username: str, id_element: str):
        try:
            assignment = AssignmentModel(
                isAssigned="true",
                assignedDate=get_date(),
                usernameAssigned=username,
                status=assignmentstatus.pending,
                reviewDate=None,
                reviewMonth=None,
                reviewYear=None
            )
            return UserController.update_assigned(username, id_element, assignment)
        except Exception as error:
            print(error)
            return None
        
    def update_assignment(self, username: str, id_element: str, status: str):
        try:
            element = ElementController.read_element(id_element)
            if element:
                assignment = element.assignment
                if status == "1": assignment.status = assignmentstatus.rediscovered
                elif status == "2": assignment.status = assignmentstatus.reviewed
                else: return False
                assignment.reviewDay = get_day()
                assignment.reviewMonth = get_month()
                assignment.reviewYear = get_year()
                return UserController.update_assigned(username, id_element, assignment)
            else: return False
        except Exception as error:
            print(error)
            return None
        
    def update_auto_assignment(self, usernames: List[str]):
        try:
            someError = False
            current_elements = ElementController.read_elements()
            elements = [element for element in current_elements if element.assignment.isAssigned == "false"]
            total_elements = len(elements)
            total_users = len(usernames)
            if total_elements % total_users == 0:
                total_assign = total_elements / total_users
                i_user = 0
                count = 0
                for element in elements:
                    if count >= total_assign:
                        i_user += 1
                        count = 0
                    username = usernames[i_user]
                    assignment = AssignmentModel(
                        isAssigned="true",
                        assignedDate=get_date(),
                        usernameAssigned=username,
                        status=assignmentstatus.pending,
                        reviewDate=None,
                        reviewMonth=None,
                        reviewYear=None
                    )
                    status = UserController.update_assigned(username, element.id, assignment)
                    if not status: someError = True
                    count += 1
                return not someError
            else:
                total_elements = total_elements - 1
                total_assign = total_elements / total_users
                i_user = 0
                count = -1
                for element in elements:
                    if count >= total_assign:
                        i_user += 1
                        count = 0
                    username = usernames[i_user]
                    assignment = AssignmentModel(
                        isAssigned="true",
                        assignedDate=get_date(),
                        usernameAssigned=username,
                        status=assignmentstatus.pending,
                        reviewDate=None,
                        reviewMonth=None,
                        reviewYear=None
                    )
                    status = UserController.update_assigned(username, element.id, assignment)
                    if not status: someError = True
                    count += 1
                return not someError                
        except Exception as error:
            print(error)
            return None
                
    def update_user_name(self, username: str, new_name: str):
        try:
            return AdminController.update_name(username, new_name.capitalize())
        except Exception as error:
            print(error)
            return None
        
    def update_user_lastname(self, username: str, new_lastname: str):
        try:
            return AdminController.update_lastname(username, new_lastname.capitalize())
        except Exception as error:
            print(error)
            return None
        
    def update_user_password(self, username: str, new_password: str):
        try:
            new_password = secure_password(new_password)
            return AdminController.update_password(username, new_password)
        except Exception as error:
            print(error)
            return None
        
    def delete_user(self, username: str):
        try:
            return AdminController.delete_user_temporal(username)
        except Exception as error:
            print(error)
            return None

    def forgot_password(self, username: str, new_password: str):
        try:
            new_password = secure_password(new_password)
            return AdminController.forgot_password(username, new_password)
        except Exception as error:
            print(error)
            return None
        
    def permission_change_password(self, username: str, permission: str):
        try:
            if permission == "true":
                return AdminController.accept_change_password(username)
            else:
                return AdminController.deny_change_password(username)
        except Exception as error:
            print(error)
            return None

Manager = ManagerResponse()