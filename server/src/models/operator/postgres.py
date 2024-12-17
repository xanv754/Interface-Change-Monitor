from typing import List
from libs.connection.postgres.connection import Postgres
from libs.connection.tables import TablesDatabase
from libs.types.account import AccountType
from libs.types.profile import ProfileType
from entities.operator import OperatorEntity, OperatorField
from models.operator.base import Operator
from models.operator.model import OperatorModel

class OperatorPostgres(Operator):
    database: Postgres

    def __init__(self):
        self.database = Postgres()
    
    def get_operator(self, username: str) -> OperatorModel | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f'SELECT * FROM {TablesDatabase.operator.value} WHERE {OperatorField.username.value} = %s', [username])
            response = cursor.fetchone()
            content = cursor.description
            if not response or not content: return None
            column_names = [column.name for column in content]
            data = dict(zip(column_names, response))
            operator = OperatorEntity(**data)
            return self.entity_to_model(operator)
        except Exception as e:
            print(e)
            return None
        
    def get_all_active(self) -> list[OperatorModel] | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f"SELECT * FROM {TablesDatabase.operator.value} WHERE {OperatorField.statusAccount.value} = '{AccountType.active.value}'")
            response = cursor.fetchall()
            if not response: return None
            content = cursor.description
            column_names = [column.name for column in content]
            operators: List[OperatorEntity] = []
            for item in response:
                data = dict(zip(column_names, item))
                operators.append(OperatorEntity(**data))
            return [self.entity_to_model(operator) for operator in operators]
        except Exception as e:
            print(e)
            return None
        
    def get_all_inactive(self) -> list[OperatorModel] | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f"SELECT * FROM {TablesDatabase.operator.value} WHERE {OperatorField.statusAccount.value} = '{AccountType.inactive.value}'")
            response = cursor.fetchall()
            if not response: return None
            content = cursor.description
            column_names = [column.name for column in content]
            operators: List[OperatorEntity] = []
            for item in response:
                data = dict(zip(column_names, item))
                operators.append(OperatorEntity(**data))
            return [self.entity_to_model(operator) for operator in operators]
        except Exception as e:
            print(e)
            return None
        
    def get_all_deleted(self) -> list[OperatorModel] | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f"SELECT * FROM {TablesDatabase.operator.value} WHERE {OperatorField.statusAccount.value} = '{AccountType.deleted.value}'")
            response = cursor.fetchall()
            if not response: return None
            content = cursor.description
            column_names = [column.name for column in content]
            operators: List[OperatorEntity] = []
            for item in response:
                data = dict(zip(column_names, item))
                operators.append(OperatorEntity(**data))
            return [self.entity_to_model(operator) for operator in operators]
        except Exception as e:
            print(e)
            return None
        
    def get_all_root(self) -> list[OperatorModel] | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f"SELECT * FROM {TablesDatabase.operator.value} WHERE {OperatorField.profile.value} = '{ProfileType.root.value}'")
            response = cursor.fetchall()
            if not response: return None
            content = cursor.description
            column_names = [column.name for column in content]
            operators: List[OperatorEntity] = []
            for item in response:
                data = dict(zip(column_names, item))
                operators.append(OperatorEntity(**data))
            return [self.entity_to_model(operator) for operator in operators]
        except Exception as e:
            print(e)
            return None
        
    def get_all_admin(self) -> list[OperatorModel] | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f"SELECT * FROM {TablesDatabase.operator.value} WHERE {OperatorField.profile.value} = '{ProfileType.admin.value}'")
            response = cursor.fetchall()
            if not response: return None
            content = cursor.description
            column_names = [column.name for column in content]
            operators: List[OperatorEntity] = []
            for item in response:
                data = dict(zip(column_names, item))
                operators.append(OperatorEntity(**data))
            return [self.entity_to_model(operator) for operator in operators]
        except Exception as e:
            print(e)
            return None
        
    def get_all_user(self) -> list[OperatorModel] | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f"SELECT * FROM {TablesDatabase.operator.value} WHERE {OperatorField.profile.value} = '{ProfileType.user.value}'")
            response = cursor.fetchall()
            if not response: return None
            content = cursor.description
            column_names = [column.name for column in content]
            operators: List[OperatorEntity] = []
            for item in response:
                data = dict(zip(column_names, item))
                operators.append(OperatorEntity(**data))
            return [self.entity_to_model(operator) for operator in operators]
        except Exception as e:
            print(e)
            return None
        
    def get_all_admin_active(self) -> list[OperatorModel] | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f"SELECT * FROM {TablesDatabase.operator.value} WHERE {OperatorField.profile.value} = '{ProfileType.admin.value}' AND {OperatorField.statusAccount.value} = '{AccountType.active.value}'")
            response = cursor.fetchall()
            if not response: return None
            content = cursor.description
            column_names = [column.name for column in content]
            operators: List[OperatorEntity] = []
            for item in response:
                data = dict(zip(column_names, item))
                operators.append(OperatorEntity(**data))
            return [self.entity_to_model(operator) for operator in operators]
        except Exception as e:
            print(e)
            return None
        
    def get_all_user_active(self) -> list[OperatorModel] | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f"SELECT * FROM {TablesDatabase.operator.value} WHERE {OperatorField.profile.value} = '{ProfileType.user.value}' AND {OperatorField.statusAccount.value} = '{AccountType.active.value}'")
            response = cursor.fetchall()
            if not response: return None
            content = cursor.description
            column_names = [column.name for column in content]
            operators: List[OperatorEntity] = []
            for item in response:
                data = dict(zip(column_names, item))
                operators.append(OperatorEntity(**data))
            return [self.entity_to_model(operator) for operator in operators]
        except Exception as e:
            print(e)
            return None
        
    def insert_operator(self, data: OperatorModel) -> OperatorModel | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f"INSERT INTO {TablesDatabase.operator.value} ( {OperatorField.username.value}, {OperatorField.name.value}, {OperatorField.lastname.value}, {OperatorField.password.value}, {OperatorField.profile.value}, {OperatorField.statusAccount.value} ) VALUES (%s, %s, %s, %s, %s, %s)",
                            (
                                data.username,
                                data.name,
                                data.lastname,
                                data.password,
                                data.profile,
                                data.statusaccount
                            )
            )
            self.database.commit()
            if cursor.rowcount >= 1:
                return self.get_operator(data.username)
            return None
        except Exception as e:
            print(e)
            return None
        
    def update_name(self, username, new_name) -> OperatorModel | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f"UPDATE {TablesDatabase.operator.value} SET {OperatorField.name.value} = %s WHERE {OperatorField.username.value} = %s", [new_name, username])
            self.database.commit()
            if cursor.rowcount >= 1:
                return self.get_operator(username)
            return None
        except Exception as e:
            print(e)        
            return None
        
    def update_lastname(self, username, new_lastname) -> OperatorModel | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f"UPDATE {TablesDatabase.operator.value} SET {OperatorField.lastname.value} = %s WHERE {OperatorField.username.value} = %s", [new_lastname, username])
            self.database.commit()
            if cursor.rowcount >= 1:
                return self.get_operator(username)
            return None
        except Exception as e:
            print(e)        
            return None
        
    def update_password(self, username, new_password) -> OperatorModel | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f"UPDATE {TablesDatabase.operator.value} SET {OperatorField.password.value} = %s WHERE {OperatorField.username.value} = %s", [new_password, username])
            self.database.commit()
            if cursor.rowcount >= 1:
                return self.get_operator(username)
            return None
        except Exception as e:
            print(e)        
            return None
        
    def update_profile(self, username, new_profile) -> OperatorModel | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f"UPDATE {TablesDatabase.operator.value} SET {OperatorField.profile.value} = %s WHERE {OperatorField.username.value} = %s", [new_profile, username])
            self.database.commit()
            if cursor.rowcount >= 1:
                return self.get_operator(username)
            return None
        except Exception as e:
            print(e)        
            return None
        
    def update_account(self, username, new_account) -> OperatorModel | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f"UPDATE {TablesDatabase.operator.value} SET {OperatorField.statusAccount.value} = %s WHERE {OperatorField.username.value} = %s", [new_account, username])
            self.database.commit()
            if cursor.rowcount >= 1:
                return self.get_operator(username)
            return None
        except Exception as e:
            print(e)        
            return None
    
    def delete(self, username: str) -> OperatorModel | None:
        try:
            operator = self.get_operator(username)
            if not operator: return None
            cursor = self.database.getCursor()
            cursor.execute(f"DELETE FROM {TablesDatabase.operator.value} WHERE {OperatorField.username.value} = %s", [username])
            self.database.commit()
            if cursor.rowcount >= 1:
                return operator
            return None
        except Exception as e:
            print(e)
            return None