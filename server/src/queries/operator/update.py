from abc import ABC, abstractmethod
from libs.types.profile import ProfileType
from libs.types.account import AccountType
from models.operator.model import OperatorModel

class UpdateOperatorQuery(ABC):
    @abstractmethod
    def update_name(self, username: str, new_name: str) -> OperatorModel | None:
        """Update the name of an operator.
        
        Parameters
        ----------
        username : str
            The username of the operator.
        new_name : str
            The new name of the operator.
        """
        pass

    @abstractmethod
    def update_lastname(self, username: str, new_lastname: str) -> OperatorModel | None:
        """Update the lastname of an operator.

        Parameters
        ----------
        username : str
            The username of the operator.
        new_lastname : str
            The new lastname of the operator. 
        """
        pass

    @abstractmethod
    def update_password(self, username: str, new_password: str) -> OperatorModel | None:
        """Update the lastname of an operator.

        Parameters
        ----------
        username : str
            The username of the operator.
        new_password : str
            The new password of the operator. 
        """
        pass

    @abstractmethod
    def update_profile(self, username: str, new_profile: ProfileType) -> OperatorModel | None:
        """Update the profile of an operator.

        Parameters
        ----------
        username : str
            The username of the operator.
        new_profile : ProfileType
            The new profile of the operator. 
        """
        pass

    @abstractmethod
    def update_account(self, username: str, new_account: AccountType) -> OperatorModel | None:
        """Update the status account of an operator.

        Parameters
        ----------
        username : str
            The username of the operator.
        new_account : AccountType
            The new status account of the operator. 
        """
        pass