from abc import ABC, abstractmethod
from models.equipment.model import EquipmentModel

class UpdateEquipmentQuery(ABC):
    @abstractmethod
    def update_community(self, id: int, new_community: str) -> EquipmentModel | None:
        """Update the community of an equipment.
        
        Parameters
        ----------
        id : int
            The ID of the equipment.
        new_community : str
            The new community of the equipment.
        """
        pass

    @abstractmethod
    def update_sysname(self, id: int, new_sysname: str) -> EquipmentModel | None:
        """Update the sysname of an equipment.
        
        Parameters
        ----------
        id : int
            The ID of the equipment.
        new_sysname : str
            The new sysname of the equipment.
        """
        pass