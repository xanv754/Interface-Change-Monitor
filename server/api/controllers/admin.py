from querys.member.update import update_account, update_name, update_lastname, update_password, update_last_password
from querys.member.find import find_type_admin, find_user, find_users_pending, find_users
from querys.member.insert import insert_user
from querys.member.delete import delete_user
from constants.userStatus import userstatus
from models.register import RegisterModel
from constants.userType import usertype
from entity.admin import Admin
from entity.user import User
from typing import List

class Admin_Controller:

    def new_admin(self, user: RegisterModel) -> Admin:
        try:
            admins = self.read_users()
            if len(admins) <= 0:
                return Admin(
                    username=user.username, 
                    password=user.password, 
                    name=user.name.capitalize(), 
                    lastname=user.lastname.capitalize(),
                    type=usertype.admin, 
                    status=userstatus.enabled
                )
            else:
                return Admin(
                    username=user.username, 
                    password=user.password, 
                    name=user.name.capitalize(), 
                    lastname=user.lastname.capitalize(),
                    type=usertype.admin, 
                    status=userstatus.pending
                )
        except Exception as error:
            print(error)
            return None
    
    def new_user(self, user: RegisterModel) -> User:
        try:
            return User(
                username=user.username,
                password=user.password, 
                name=user.name.capitalize(), 
                lastname=user.lastname.capitalize(),
                type=usertype.user, 
                status=userstatus.pending
            )
        except Exception as error:
            print(error)
            return None

    def read_users(self) -> List[Admin]:
        try:
            return find_type_admin()
        except Exception as error:
            print(error)
            return None
        
    def read_admin(self, username: str) -> Admin:
        try:
            return find_user(username)
        except Exception as error:
            print(error)
            return None
        
    def read_users_pending(self) -> list:
        try:
            return find_users_pending()
        except Exception as error:
            print(error)
            return []
        
    def read_all_users(self) -> list:
        try:
            return find_users()
        except Exception as error:
            print(error)
            return []
        
    def create_admin(self, new_admin: Admin) -> bool:
        try:
            res = insert_user(new_admin)
            if res: return res.acknowledged
            else: return False
        except Exception as error:
            print(error)
            return None
        
    def create_user(self, new_user: User) -> bool:
        try:
            res = insert_user(new_user)
            if res: return res.acknowledged
            else: return False
        except Exception as error:
            print(error)
            return None
        
    def delete_user(self, username: str) -> bool:
        try:
            res = delete_user(username)
            if res: return res.acknowledged
            else: return False
        except Exception as error:
            print(error)
            return None
        
    def delete_user_temporal(self, username: str) -> bool:
        try:
            res = update_account(username, userstatus.disabled)
            if res: return res.acknowledged
            else: return False
        except Exception as error:
            print(error)
            return None
        
    def restore_user(self, username: str) -> bool:
        try:
            res = update_account(username, userstatus.enabled)
            if res: return res.acknowledged
            else: return False
        except Exception as error:
            print(error)
            return None
        
    def accept_user(self, username: str) -> bool:
        try:
            res = update_account(username, userstatus.enabled)
            if res: return res.acknowledged
            else: return False
        except Exception as error:
            print(error)
            return None

    def search_user(self, username: str) -> (User | Admin):
        try:
            return find_user(username)
        except Exception as error:
            print(error)
            return None
        
    def update_name(self, username: str, new_name: str) -> bool:
        try:
            res = update_name(username, new_name)
            if res: return res.acknowledged
            else: return False
        except Exception as error:
            print(error)
            return None
        
    def update_lastname(self, username: str, new_lastname: str) -> bool:
            try:
                res = update_lastname(username, new_lastname)
                if res: return res.acknowledged
                else: return False
            except Exception as error:
                print(error)
                return None
        
    def update_password(self, username: str, password: str) -> bool:
        try:
            res = update_password(username, password)
            if res: return res.acknowledged
            else: return False
        except Exception as error:
            print(error)
            return None
        
    def forgot_password(self, username: str, password: str) -> bool:
        try:
            user = find_user(username)
            if user and user.status == userstatus.enabled:
                changeUserStatus = update_account(username, userstatus.password_pending)
                if changeUserStatus: 
                    backupPasswordStatus = update_last_password(username, user.password)
                    if backupPasswordStatus and backupPasswordStatus.acknowledged:
                        changePasswordStatus = update_password(username, password)
                        if changePasswordStatus: return changePasswordStatus.acknowledged
            return False
        except Exception as error:
            print(error)
            return None
        
    def accept_change_password(self, username: str) -> bool:
        try:
            user = find_user(username)
            if user and user.status == userstatus.password_pending:
                res = update_account(username, userstatus.enabled)
                if res: return res.acknowledged
            return False
        except Exception as error:
            print(error)
            return None
        
    def deny_change_password(self, username: str) -> bool:
        try:
            user = find_user(username)
            if user and user.status == userstatus.password_pending:
                restore_password_status = update_password(username, user.lastPassword)
                if restore_password_status and restore_password_status.acknowledged:
                    change_user_status = update_account(username, userstatus.enabled)
                    if change_user_status: return change_user_status.acknowledged
            return False
        except Exception as error:
            print(error)
            return None

AdminController = Admin_Controller()