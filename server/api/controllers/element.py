from querys.element.find import find_elements_backup, find_elements, find_element, find_elements_by_month_assigment
from querys.element.delete import delete_elements, delete_element, delete_elements_by_month
from controllers.interface import InterfaceController
from querys.element.update import update_assignment
from querys.element.insert import insert_elements
from controllers.backup import BackupController
from utils.validator import change_validator
from models.assignment import AssignmentModel
from models.interface import InterfaceModel
from entity.element import Element
from utils.date import get_date
from typing import List

class Element_Controller:
    def __create_new_elements(self) -> List[Element]:
        try:
            new_elements: List[Element] = []
            current_interfaces: List[Element] = InterfaceController.read_interfaces()
            if not current_interfaces: return None
            for interface in current_interfaces:
                backup_interface = BackupController.read_interface(interface.ip, interface.community, interface.ifIndex)
                if backup_interface:
                    changes = change_validator(interface, backup_interface)
                    if changes:
                        new_assigment = AssignmentModel()
                        new_element = Element(old=backup_interface, current=interface, date=get_date(), assignment=new_assigment)
                        new_elements.append(new_element)
            return new_elements
        except Exception as error:
            print("ERROR: No se obtuvo la información para crear los nuevos elementos")
            print(error)
            return None
        
    def read_elements_backup(self) -> List[Element]:
        try:
            return find_elements_backup()
        except Exception as error:
            print(error)
            return None
        
    def read_elements_by_month(self, month: str) -> List[Element]:
        try:
            return find_elements_by_month_assigment(month)
        except Exception as error:
            print(error)
            return None
    
    def read_elements(self) -> List[Element]:
        try:
            return find_elements()
        except Exception as error:
            print(error)
            return None
            
    def read_element(self, id: str) -> Element:
        try:
            return find_element(id)
        except Exception as error:
            print(error)
            return None
        
    def read_interface_element(self, id: str) -> InterfaceModel:
        try:
            element = find_element(id)
            if element: return InterfaceModel(
                idElement=element.id, 
                ip=element.current.ip, 
                community=element.current.community,
                assignment=element.assignment
            )
            else: return None
        except Exception as error:
            print(error)
            return None
        
    def create_elements(self, elements: List[Element]) -> bool:
        try:
            res = insert_elements(elements)
            if res: return res.acknowledged
            else: return False
        except Exception as error:
            print(error)
            return None

    def delete_elements(self) -> bool:
        try:
            res = delete_elements()
            if res: return res.acknowledged
            else: return False
        except Exception as error:
            print(error)
            return None
        
    def delete_elements_by_month(self, month: str) -> bool:
        try:
            res = delete_elements_by_month(month)
            if res: return res.acknowledged
            else: return False
        except Exception as error:
            print(error)
            return None
        
    def delete_element(self, id: str) -> bool:
        try:
            res = delete_element(id)
            if res: return res.acknowledged
            else: return False
        except Exception as error:
            print(error)
            return None

    def update_assignment(self, id: str, assignment: AssignmentModel) -> bool:
        try:
            element = find_element(id)
            if not element: return False
            status = update_assignment(id, assignment)
            if status: return status.acknowledged
            else: return False
        except Exception as error:
            print(error)
            return None
    
    def load_elements(self) -> bool: 
        try:
            elements = self.__create_new_elements()
            if elements: return self.create_elements(elements)
            else: return False
        except Exception as error:
            print("ERROR: No se pudieron cargar los nuevos elementos")
            print(error)
            return None

ElementController = Element_Controller()
                