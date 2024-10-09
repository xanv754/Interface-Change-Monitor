from querys.interface.find import find_backup, find_interface_backup
from querys.interface.delete import delete_backup
from querys.interface.insert import insert_backup
from entity.interface import Interface
from typing import List

class Backup_Controller:
    def read_interfaces(self) -> List[Interface]:
        try:
            return find_backup()
        except Exception as error:
            print(error)
            return None

    def read_interface(self, ip: str, community: str, ifIndex: str) -> Interface:
        try:
            return find_interface_backup(ip, community, ifIndex)
        except Exception as error:
            print(error)
            return None
                    
    def create_backup(self, data: List[Interface]) -> bool:
        try:
            delete_backup()
            res = insert_backup(data)
            if res: return res.acknowledged
            else: return False
        except Exception as error:
            print(error)
            return None
    
BackupController = Backup_Controller()