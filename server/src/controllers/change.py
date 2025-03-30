from typing import List
from database.models.change import ChangeModel
from schemas.change import ChangeInterfaceSchema, RegisterChangeBody
from utils.log import LogHandler


class ChangeController:
    """Controller for all operations of change table."""

    @staticmethod
    def get_all_changes() -> List[ChangeInterfaceSchema]:
        """Get all changes of the system."""
        try:
            return ChangeModel.get_changes()
        except Exception as e:
            LogHandler(content=f"Changes not obtained. {e}", path=__file__, err=True)
            return []

    @staticmethod
    def register(changes: List[RegisterChangeBody]) -> bool:
        """Register new changes in the system."""
        try:
            return ChangeModel.register(changes)
        except Exception as e:
            LogHandler(content=f"Changes not registered. {e}", path=__file__, err=True)
            return False

    @staticmethod
    def update_operator(ids: List[int], operator: str) -> bool:
        """Update the operator of the assigned of the changes.

        Parameters
        ----------
        ids : List[int]
            List of IDs of the changes.
        operator : str
            New operator of the changes.
        """
        try:
            return ChangeModel.update_assigned(ids, operator)
        except Exception as e:
            LogHandler(content=f"Changes not updated. {e}", path=__file__, err=True)
            return False

    @staticmethod
    def delete() -> bool:
        """Delete all changes of the system."""
        try:
            return ChangeModel.reset_changes()
        except Exception as e:
            LogHandler(content=f"Changes not deleted. {e}", path=__file__, err=True)
            return False
