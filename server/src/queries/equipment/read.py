from abc import ABC, abstractmethod
from models.equipment.model import EquipmentModel

class ReadEquipmentQuery(ABC):
    @abstractmethod
    def get_equipment(self, id: int) -> EquipmentModel | None:
        """Get an equipment by id.
        
        Parameters
        ----------
        id : int
            The ID of the equipment.
        """
        pass

    @abstractmethod
    def get_equipment_by_info(self, ip: str, community: str) -> EquipmentModel | None:
        """Get an equipment by its IP and community information.
        
        Parameters
        ----------
        ip : str
            The IP of the equipment.
        community : str
            The community of the equipment.
        """
        pass