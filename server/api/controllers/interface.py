from querys.interface.delete import delete_interfaces
from querys.interface.insert import insert_interfaces
from querys.interface.find import find_interfaces
from controllers.backup import BackupController
from entity.interface import Interface
from constants.base import constants
from utils.data import create_data
from typing import List
from os import listdir
import json

class Interface_Controller:

    def __extract_data(self) -> List[Interface]:
        try:
            new_interfaces: List[Interface] = []
            files = listdir(constants.FILEPATH)
            if '.gitkeep' in files: files.remove('.gitkeep')
            for path in files:
                with open(f'{constants.FILEPATH}/{path}') as file:
                    data = json.load(file)
                    interfaces = data['snmp']
                    new_interfaces = create_data(interfaces)
            return new_interfaces
        except FileNotFoundError:
            print('WARNING: File with the data not found')
        except Exception as e:
            raise Exception(e)
        
    def read_interfaces(self) -> List[Interface]:
        try:
            return find_interfaces()
        except Exception as error:
            print(error)
            return None

    def create_interfaces(self, interfaces: List[Interface]) -> bool:
        try:
            res = insert_interfaces(interfaces)
            if res: return res.acknowledged
            else: return False
        except Exception as error:
            print(error)
            return None

    def delete_interfaces(self) -> bool:
        try:
            res = delete_interfaces()
            return res.acknowledged
        except Exception as error:
            print(error)
            return None
            
    def load_data(self) -> bool:
        try:
            new_interfaces = self.__extract_data()
            if new_interfaces:
                old_interfaces = self.read_interfaces()
                if old_interfaces:
                    if BackupController.create_backup(old_interfaces) and self.delete_interfaces():
                        return self.create_interfaces(new_interfaces)
                else: return self.create_interfaces(new_interfaces)
            else: return False
        except Exception as error:
            print("ERROR: No se logró actualizar la base de datos de las interfaces")
            print(error)
            return None

InterfaceController = Interface_Controller()