from abc import ABC, abstractmethod
from models.operator.model import OperatorModel

class DeleteOperatorQuery(ABC):
    @abstractmethod
    def delete(self, username: str) -> OperatorModel | None:
        """Delete an operator.
        
        Parameters
        ----------
        username : str
            The username of the operator.
        """
        pass