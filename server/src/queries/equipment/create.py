from abc import ABC, abstractmethod
from models.equipment.model import EquipmentModel

class CreateEquipmentQuery(ABC):
    @abstractmethod
    def insert(self, data: EquipmentModel) -> EquipmentModel | None:
        """Insert an new equipment.
        
        Parameters
        ----------
        data : EquipmentModel
            The data of the equipment to be inserted.
        """
        pass