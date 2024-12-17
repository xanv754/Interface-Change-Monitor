from abc import ABC, abstractmethod
from models.operator.model import OperatorModel

class ReadOperatorQuery(ABC):
    @abstractmethod
    def get_operator(self, username: str) -> OperatorModel | None:
        """Get an operator by username.
        
        Parameters
        ----------
        username : str
            The username of the operator.
        """
        pass

    @abstractmethod
    def get_all_active(self) -> list[OperatorModel] | None:
        """Get all active operators."""
        pass

    @abstractmethod
    def get_all_inactive(self) -> list[OperatorModel] | None:
        """Get all inactive operators."""
        pass

    @abstractmethod
    def get_all_deleted(self) -> list[OperatorModel] | None:
        """Get all deleted operators."""
        pass

    @abstractmethod
    def get_all_root(self) -> list[OperatorModel] | None:
        """Get all super admins operators."""
        pass

    @abstractmethod
    def get_all_admin(self) -> list[OperatorModel] | None:
        """Get all admins operators."""
        pass

    @abstractmethod
    def get_all_user(self) -> list[OperatorModel] | None:
        """Get all standard users operators."""
        pass

    @abstractmethod
    def get_all_admin_active(self) -> list[OperatorModel] | None:
        """Get all active admins operators."""
        pass

    @abstractmethod
    def get_all_user_active(self) -> list[OperatorModel] | None:
        """Get all active standard users operators."""
        pass