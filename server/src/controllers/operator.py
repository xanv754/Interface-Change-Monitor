from libs.types.profile import ProfileType
from libs.types.account import AccountType
from models.operator.postgres import OperatorPostgres
from models.operator.model import OperatorModel

class OperatorController:
    def get(self, username: str) -> dict | None:
        model = OperatorPostgres()
        response = model.get_operator(username)
        if response:
            return response.model_dump()
        return None
    
    def get_all_active(self) -> list[dict] | None:
        model = OperatorPostgres()
        response = model.get_all_active()
        if response:
            return [operator.model_dump() for operator in response]
        return None
    
    def get_all_inactive(self) -> list[dict] | None:
        model = OperatorPostgres()
        response = model.get_all_inactive()
        if response:
            return [operator.model_dump() for operator in response]
        return None
    
    def get_all_deleted(self) -> list[dict] | None:
        model = OperatorPostgres()
        response = model.get_all_deleted()
        if response:
            return [operator.model_dump() for operator in response]
        return None
    
    def get_all_root(self) -> list[dict] | None:
        model = OperatorPostgres()
        response = model.get_all_root()
        if response:
            return [operator.model_dump() for operator in response]
        return None
    
    def get_all_admin(self) -> list[dict] | None:
        model = OperatorPostgres()
        response = model.get_all_admin()
        if response:
            return [operator.model_dump() for operator in response]
        return None
    
    def get_all_user(self) -> list[dict] | None:
        model = OperatorPostgres()
        response = model.get_all_user()
        if response:
            return [operator.model_dump() for operator in response]
        return None

    def get_all_admin_active(self) -> list[dict] | None:
        model = OperatorPostgres()
        response = model.get_all_admin_active()
        if response:
            return [operator.model_dump() for operator in response]
        return None
    
    def get_all_user_active(self) -> list[dict] | None:
        model = OperatorPostgres()
        response = model.get_all_user_active()
        if response:
            return [operator.model_dump() for operator in response]
        return None  
    
    def insert(self, data: OperatorModel) -> dict | None:
        model = OperatorPostgres()
        response = model.insert_operator(data)
        if response:
            return response.model_dump()
        return None
    
    def update_name(self, username: str, new_name: str) -> dict | None:
        model = OperatorPostgres()
        response = model.update_name(username, new_name)
        if response:
            return response.model_dump()
        return None
    
    def update_lastname(self, username: str, new_lastname: str) -> dict | None:
        model = OperatorPostgres()
        response = model.update_lastname(username, new_lastname)
        if response:
            return response.model_dump()
        return None
    
    def update_password(self, username: str, new_password: str) -> dict | None:
        model = OperatorPostgres()
        response = model.update_password(username, new_password)
        if response:
            return response.model_dump()
        return None
    
    def update_profile(self, username: str, new_profile: ProfileType) -> dict | None:
        model = OperatorPostgres()
        response = model.update_profile(username, new_profile)
        if response:
            return response.model_dump()
        return None

    def update_account(self, username: str, new_account: AccountType) -> dict | None:
        model = OperatorPostgres()
        response = model.update_account(username, new_account)
        if response:
            return response.model_dump()
        return None
    
    def delete_hard(self, username: str) -> dict | None:
        model = OperatorPostgres()
        response = model.delete(username)
        if response:
            return response.model_dump()
        return None