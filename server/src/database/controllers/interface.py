from typing import List
from datetime import datetime, timedelta
from error import ErrorHandler, ErrorInterfaceHandler, CODEINTERFACE
from database.constants.types.interface import Date
from database.entities.interface import InterfaceField
from database.entities.equipment import EquipmentField
from database.models.interface import InterfaceModel
from database.models.equipment import EquipmentModel
from database.utils import create
from database.utils.json import interface_to_json

class InterfaceController:
    @staticmethod
    def read_interface(id: int) -> list | ErrorHandler:
        """Returns a list with an interface.
        
        Parameters
        ----------
        id: int
            Interface ID.
        """
        try:
            return interface_to_json([InterfaceModel.get_interface_by_id(id)])
        except Exception as e:
            error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    @staticmethod
    def read_interfaces() -> list | ErrorHandler:
        """Returns a list with all interfaces."""
        try:
            return interface_to_json(InterfaceModel.get_interfaces())
        except Exception as e:
            error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    @staticmethod
    def read_interfaces_by_equipment(ip: str, community: str) -> list | ErrorHandler:
        """Returns a list with all interfaces of an equipment.
        
        Parameters
        ----------
        ip: str
            Equipment IP.
        community: str
            Equipment community.
        """
        try:
            equipment = EquipmentModel.get_equipment_by_ip_and_community(ip, community)
            if not equipment:
                return ErrorInterfaceHandler(CODEINTERFACE.ERROR_404_EQUIPMENT_NOT_FOUND)
            else:
                return interface_to_json(InterfaceModel.get_interfaces_by_equipment(equipment.id))
        except Exception as e:
            error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    @staticmethod
    def read_interface_by_index(ip: str, community: str, index: int) -> list | ErrorHandler:
        """Returns a list with an interface of an equipment.
        
        Parameters
        ----------
        ip: str
            Equipment IP.
        community: str
            Equipment community.
        index: int
            Interface ifIndex.
        """
        try:
            equipment = EquipmentModel.get_equipment_by_ip_and_community(ip, community)
            if not equipment:
                return ErrorInterfaceHandler(CODEINTERFACE.ERROR_404_EQUIPMENT_NOT_FOUND)
            else:
                return interface_to_json([InterfaceModel.get_interfaces_by_index(equipment.id, index)])
        except Exception as e:
            error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error

    @staticmethod
    def read_interfaces_by_date_consult(date_consult: str) -> list | ErrorHandler:
        """Returns a list with all interfaces filters by your date of consult.
        
        Parameters
        ----------
        date_consult: str
            Date of consult in format YYYY-MM-DD.
        """
        try:
            return interface_to_json(InterfaceModel.get_interfaces_by_date_consult(date_consult))
        except Exception as e:
            error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    @staticmethod
    def read_interfaces_today() -> list | ErrorHandler:
        """Returns a list with all interfaces filters by date type. The date type is equal to TODAY."""
        try:
            return interface_to_json(InterfaceModel.get_interfaces_today())
        except Exception as e:
            error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    @staticmethod
    def read_interfaces_yesterday() -> list | ErrorHandler:
        """Returns a list with all interfaces filters by date type. The date type is equal to YESTERDAY."""
        try:
            return interface_to_json(InterfaceModel.get_interfaces_yesterday())
        except Exception as e:
            error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
    
    @staticmethod
    def read_interfaces_old() -> list | ErrorHandler:
        """Returns a list with all interfaces filters by date type. The date type is equal to OLD."""
        try:
            return interface_to_json(InterfaceModel.get_interfaces_old())
        except Exception as e:
            error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    @staticmethod
    def create_interface(ip: str, community: str, body: dict, sysname: str | None = None) -> list | ErrorHandler:
        """Creates an interface. If the equipment doesn't exist, it is created.
        
        Parameters
        ----------
        body: dict
            Dict with the values of the interface to be created.
        """
        try:
            equipment = EquipmentModel.get_equipment_by_ip_and_community(ip, community)
            if not equipment:
                if not sysname: 
                    return ErrorInterfaceHandler(CODEINTERFACE.ERROR_400_SYSNAME_REQUIRED)
                else:
                    new_equipment = {
                        EquipmentField.ip.value: ip,
                        EquipmentField.community.value: community,
                        EquipmentField.sysname.value: sysname
                    }
                    equipment = EquipmentModel.insert_equipment(new_equipment)
                    if not equipment:
                        error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_404_EQUIPMENT_NOT_INSERTED)
                        create.log(error, f"Equipment not created. Tried to insert, but failed: {ip}, {community}")
                        return error
                    else:
                        body[{InterfaceField.idEquipment.value}] = equipment.id
                        return interface_to_json([InterfaceModel.insert_interface(body)])
            else:
                body[{InterfaceField.idEquipment.value}] = equipment.id
                return interface_to_json([InterfaceModel.insert_interface(body)])
        except Exception as e:
            error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    # @staticmethod
    # def create_interfaces(data: List[dict]) -> int | ErrorHandler:
    #     """Create multiple interfaces. If the equipment doesn't exist, it is created.

    #     Parameters
    #     ----------
    #     data: List[dict]
    #         List of dict with the values of the interfaces to be created.
    #     """
    #     try:
    #         interfaces_valid: List[dict] = []
    #         for current_interface in data:
    #             keys = current_interface.keys()
    #             if {EquipmentField.ip.value} in keys and {EquipmentField.community.value} in keys:
    #                 ip = current_interface[{EquipmentField.ip.value}]
    #                 community = current_interface[{EquipmentField.community.value}]
    #                 equipment = EquipmentModel.get_equipment_by_ip_and_community(ip, community)
    #                 if equipment:
    #                     del current_interface[{EquipmentField.ip.value}]
    #                     del current_interface[{EquipmentField.community.value}]
    #                     if {EquipmentField.sysname.value} in keys:
    #                         del current_interface[{EquipmentField.sysname.value}]
    #                     current_interface[{InterfaceField.idEquipment.value}] = equipment.id
    #                     interfaces_valid.append(current_interface)
    #                 else:
    #                     if {EquipmentField.sysname.value} in keys:
    #                         sysname = current_interface[{EquipmentField.sysname.value}]
    #                         new_equipment = {
    #                             EquipmentField.ip.value: ip,
    #                             EquipmentField.community.value: community,
    #                             EquipmentField.sysname.value: sysname
    #                         }
    #                         equipment = EquipmentModel.insert_equipment(new_equipment)
    #                         if not equipment: 
    #                             create.log(error_console=f"Equipment not created. Tried to insert, but failed: {ip}, {community}")
    #                             continue
    #                         del current_interface[{EquipmentField.ip.value}]
    #                         del current_interface[{EquipmentField.community.value}]
    #                         del current_interface[{EquipmentField.sysname.value}]
    #                         current_interface[EquipmentField.id.value] = equipment.id
    #                         interfaces_valid.append(current_interface)
    #                     else:
    #                         create.log(ErrorInterfaceHandler(CODEINTERFACE.ERROR_400_SYSNAME_REQUIRED), f"Equipment not created: {ip}, {community}")
    #                         continue
    #             else: continue
    #         return InterfaceModel.insert_interfaces(interfaces_valid)
    #     except Exception as e:
    #         error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
    #         create.log(error, e)
    #         return error
        
    def delete_interface(id_equipment: int, if_index: int) -> bool:
        """Returns the deletion status of an interface.

        Parameters
        ----------
        id_equipment: int
            Equipment ID.
        if_index: int
        """
        try:
            return InterfaceModel.delete_interface(id_equipment, if_index)
        except Exception as e:
            error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    # def delete_interfaces_by_equipment(data: List[tuple]) -> int:
    #     """Returns the deletion status of a list of interfaces by equipment ID and ifIndex.

    #     Parameters
    #     ----------
    #     data: List[tuple]
    #         List of tuples with the values of the interfaces to be deleted.
    #         (idEquipment, ifIndex)
    #     """
    #     try:
    #         return InterfaceModel.delete_interfaces_by_equipment(data)
    #     except Exception as e:
    #         error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
    #         create.log(error, e)
    #         return error
        
    def delete_interfaces_by_id(data: List[int]) -> int:
        """Returns the deletion status of a list of interfaces by id.

        Parameters
        ----------
        data: List[int]
            List of ids of the interfaces to be deleted.
        """
        try:
            return InterfaceModel.delete_interfaces_by_id(data)
        except Exception as e:
            error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    def delete_interfaces_by_date_consult(date_consult: str) -> int:
        """Returns the deletion status of a list of interfaces by date of consult.

        Parameters
        ----------
        date_consult: str
            Date of consult in format YYYY-MM-DD.
        """
        try:
            return InterfaceModel.delete_interfaces_by_date_consult(date_consult)
        except Exception as e:
            error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    def update_interface_today(body: dict) -> bool:
        """Returns the status of the update of an interface with the type date TODAY.

        Parameters
        ----------
        data: dict
            Dict with the values of the interface to be updated.
        """
        try:
            interface = InterfaceModel.get_interface_by_id(id)
            if not interface:
                return ErrorInterfaceHandler(CODEINTERFACE.ERROR_404_INTERFACE_NOT_FOUND)
            else:
                body[{InterfaceField.id.value}] = interface.id
                body[{InterfaceField.idEquipment.value}] = interface.idEquipment
                body[{InterfaceField.ifIndex.value}] = interface.ifIndex
                body[{InterfaceField.dateConsult.value}] = datetime.now().strftime("%Y-%m-%d")
                body[{InterfaceField.dateType.value}] = Date.TODAY.value
                return InterfaceModel.update_interface(body)
        except Exception as e:
            error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
    
    def update_interface_yesterday(body: dict) -> bool:
        """Returns the status of the update of an interface with the type date YESTERDAY.

        Parameters
        ----------
        data: dict
            Dict with the values of the interface to be updated.
        """
        try:
            interface = InterfaceModel.get_interface_by_id(id)
            if not interface:
                return ErrorInterfaceHandler(CODEINTERFACE.ERROR_404_INTERFACE_NOT_FOUND)
            else:
                date_yesterday = datetime.now() - timedelta(days=1)
                body[{InterfaceField.id.value}] = interface.id
                body[{InterfaceField.idEquipment.value}] = interface.idEquipment
                body[{InterfaceField.ifIndex.value}] = interface.ifIndex
                body[{InterfaceField.dateConsult.value}] = date_yesterday.strftime("%Y-%m-%d")
                body[{InterfaceField.dateType.value}] = Date.YESTERDAY.value
                return InterfaceModel.update_interface(body)
        except Exception as e:
            error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    def update_type_date_to_yesterday() -> bool:
        try:
            return InterfaceModel.update_type_date_to_yesterday()
        except Exception as e:
            error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error
        
    def update_type_date_to_old() -> bool:
        try:
            return InterfaceModel.update_type_date_to_old()
        except Exception as e:
            error = ErrorInterfaceHandler(CODEINTERFACE.ERROR_500_UNKNOWN)
            create.log(error, e)
            return error