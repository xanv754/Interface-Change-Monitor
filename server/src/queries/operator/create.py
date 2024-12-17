from abc import ABC, abstractmethod
from models.operator.model import OperatorModel

class CreateOperatorQuery(ABC):
    @abstractmethod
    def insert_operator(self, data: OperatorModel) -> OperatorModel | None:
        """Insert an operator.
        
        Parameters
        ----------
        data : OperatorModel
            The data of the operator to be inserted.
        """
        pass