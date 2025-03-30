from constants.types import InterfaceType, StatusType, StatusAssignmentType, AccountType, ProfileType


class ValidDataHandler:
    """Handler to valid data to the system."""

    @staticmethod
    def interface_type(value: str) -> bool:
        """Check if a string is a valid interface type.

        Parameters
        ----------
        value : str
            String to be checked.
        """
        return value in InterfaceType._value2member_map_

    @staticmethod
    def status_type(value: str) -> bool:
        """Check if a string is a valid status type.

        Parameters
        ----------
        value : str
            String to be checked.
        """
        return value in StatusType._value2member_map_

    @staticmethod
    def status_assignment_type(value: str) -> bool:
        """Check if a string is a valid status assignment type.

        Parameters
        ----------
        value : str
            String to be checked.
        """
        return value in StatusAssignmentType._value2member_map_

    @staticmethod
    def account_type(value: str) -> bool:
        """Check if a string is a valid account type.

        Parameters
        ----------
        value : str
            String to be checked.
        """
        return value in AccountType._value2member_map_

    @staticmethod
    def profile_type(value: str) -> bool:
        """Check if a string is a valid profile type.

        Parameters
        ----------
        value : str
            String to be checked.
        """
        return value in ProfileType._value2member_map_
