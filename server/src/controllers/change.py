from typing import List
from database import Change, ChangeModel
from schemas import ChangeInterfaceSchema, RegisterChangeBody
from utils import Log

class ChangeController:
    """Controller of notificacions of changes."""

    @staticmethod
    def get_all_changes() -> List[ChangeInterfaceSchema]:
        """Get all changes of the system."""
        try:
            return Change.get_all_changes()
        except Exception as e:
            Log.save(f"Changes not obtained. {e}", __file__, Log.error)
            return []

    @staticmethod
    def register(changes: List[RegisterChangeBody]) -> bool:
        """Register new changes in the system."""
        try:
            return ChangeModel.register(changes)
        except Exception as e:
            Log.save(f"Changes not registered. {e}", __file__, Log.error)
            return False

    @staticmethod
    def update_operator(ids: List[int], operator: str) -> bool:
        """Update the operator of the assigned of the changes. \n
        Note: Its necessary declare the ID change in the constructor.

        Parameters
        ----------
        ids: List[int]
            List of IDs of the changes.
        operator : str
            New operator of the changes.
        """
        try:
            model = Change(username=operator)
            return model.update_assigned(ids)
        except Exception as e:
            Log.save(f"Changes not updated. {e}", __file__, Log.error)
            return False

    @staticmethod
    def delete() -> bool:
        """Delete all changes of the system."""
        try:
            return Change.reset_changes()
        except Exception as e:
            Log.save(f"Changes not deleted. {e}", __file__, Log.error)
            return False
