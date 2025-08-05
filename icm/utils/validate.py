from datetime import datetime
from icm.constants import RoleTypes, UserStatusTypes, AssignmentStatusTypes


class Validate:
    """Class to manage validation."""

    @staticmethod
    def date(date: str) -> bool:
        """Validate date.
        
        Parameters
        ----------
        date : str
            Date to validate.

        Returns
        -------
        bool
            True if the date is valid, False otherwise.
        """
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except:
            return False
        
    @staticmethod
    def month_date(date: str) -> bool:
        try:
            datetime.strptime(date, "%Y-%m")
            return True
        except:
            return False

    @staticmethod
    def role(role: str) -> bool:
        """Validate role.
        
        Parameters
        ----------
        role : str
            Role to validate.

        Returns
        -------
        bool
            True if the role is valid, False otherwise.
        """
        return role in [RoleTypes.ADMIN, RoleTypes.ROOT, RoleTypes.USER, RoleTypes.SOPORT]
    
    @staticmethod
    def status(status: str) -> bool:
        """Validate status.
        
        Parameters
        ----------
        status : str
            Status to validate.

        Returns
        -------
        bool
            True if the status is valid, False otherwise.
        """
        return status in [UserStatusTypes.ACTIVE, UserStatusTypes.INACTIVE, UserStatusTypes.DELETED]

    @staticmethod
    def assignment_status(status: str) -> bool:
        """Validate assignment status.
        
        Parameters
        ----------
        status : str
            Status to validate.

        Returns
        -------
        bool
            True if the status is valid, False otherwise.
        """
        return status in [AssignmentStatusTypes.PENDING, AssignmentStatusTypes.INSPECTED, AssignmentStatusTypes.REDISCOVERED]