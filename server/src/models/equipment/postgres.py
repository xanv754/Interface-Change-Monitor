from typing import List
from libs.connection.postgres.connection import Postgres
from libs.connection.tables import TablesDatabase
from entities.equipment import EquipmentEntity, EquipmentField
from models.equipment.base import Equipment
from models.equipment.model import EquipmentModel
from queries.operator import delete

class EquipmentPostgres(Equipment):
    database: Postgres

    def __init__(self):
        self.database = Postgres()

    def get_equipment(self, id) -> EquipmentModel | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f'SELECT * FROM {TablesDatabase.equipment.value} WHERE {EquipmentField.id.value} = %s', [id])
            response = cursor.fetchone()
            content = cursor.description
            if not response or not content: return None
            column_names = [column.name for column in content]
            data = dict(zip(column_names, response))
            operator = EquipmentEntity(**data)
            return self.entity_to_model(operator)
        except Exception as e:
            print(e)
            return None
        
    def get_equipment_by_info(self, ip, community) -> EquipmentModel | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f'SELECT * FROM {TablesDatabase.equipment.value} WHERE {EquipmentField.ip.value} = %s AND {EquipmentField.community.value} = %s', [ip, community])
            response = cursor.fetchone()
            content = cursor.description
            if not response or not content: return None
            column_names = [column.name for column in content]
            data = dict(zip(column_names, response))
            operator = EquipmentEntity(**data)
            return self.entity_to_model(operator)
        except Exception as e:
            print(e)
            return None

    def insert(self, data: EquipmentModel) -> EquipmentModel | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f"INSERT INTO {TablesDatabase.equipment.value} ( {EquipmentField.ip.value}, {EquipmentField.community.value}, {EquipmentField.sysname.value} ) VALUES (%s, %s, %s)",
                            (
                                data.ip,
                                data.community,
                                data.sysname
                            )
            )
            self.database.commit()
            if cursor.rowcount >= 1:
                return self.get_equipment_by_info(data.ip, data.community)
            return None
        except Exception as e:
            print(e)
            return None
        
    def update_community(self, id, new_community) -> EquipmentModel | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f"UPDATE {TablesDatabase.equipment.value} SET {EquipmentField.community.value} = %s WHERE {EquipmentField.id.value} = %s", [new_community, id])
            self.database.commit()
            if cursor.rowcount >= 1:
                return self.get_equipment(id)
            return None
        except Exception as e:
            print(e)
            return None
        
    def update_sysname(self, id, new_sysname) -> EquipmentModel | None:
        try:
            cursor = self.database.getCursor()
            cursor.execute(f"UPDATE {TablesDatabase.equipment.value} SET {EquipmentField.sysname.value} = %s WHERE {EquipmentField.id.value} = %s", [new_sysname, id])
            self.database.commit()
            if cursor.rowcount >= 1:
                return self.get_equipment(id)
            return None
        except Exception as e:
            print(e)
            return None 
        
    def delete(self, id) -> EquipmentModel | None:
        try:
            operator = self.get_equipment(id)
            if not operator: return None
            cursor = self.database.getCursor()
            cursor.execute(f"DELETE FROM {TablesDatabase.equipment.value} WHERE {EquipmentField.id.value} = %s", [id])
            self.database.commit()
            if cursor.rowcount >= 1:
                return operator
            return None
        except Exception as e:
            print(e)
            return None