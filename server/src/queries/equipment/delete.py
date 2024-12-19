from abc import ABC, abstractmethod
from models.equipment.model import EquipmentModel
from queries.operator import delete

class DeleteEquipmentQuery(ABC):
    @abstractmethod
    def delete(self, id: int) -> EquipmentModel | None:
        """Delete an equipment.
        
        Parameters
        ----------
        id : int
            The ID of the equipment.
        """
        pass