from typing import List
from core import SystemConfig
from models import ChangesModel
from schemas import SystemConfigResponse, ChangesResponse
from utils import Log

class SystemController:
    """Controller of the configuration of the system."""

    @staticmethod
    def get_system_config() -> SystemConfigResponse | None:
        """Get the settings of the system."""
        try:
            system_config = SystemConfig()
            return system_config.get_system_config()
        except Exception as e:
            Log.save(f"System configuration not obtained. {e}", __file__, Log.error)
            return None
        
    @staticmethod
    def update_config(config: SystemConfigResponse) -> bool:
        """Update the settings of the system.
        
        Parameters
        ----------
        config : SystemConfigSchema
            New settings of the system.
        """
        try:
            system_config = SystemConfig()
            return system_config.update_config(config)
        except Exception as e:
            Log.save(f"System configuration not updated. {e}", __file__, Log.error)
            return False
        
    @staticmethod
    def get_all_changes() -> List[ChangesResponse]:
        """Get all changes of the system."""
        try:
            return ChangesModel.get_all_changes()
        except Exception as e:
            Log.save(f"Changes not obtained. {e}", __file__, Log.error)
            return []
        
    @staticmethod
    def register_change(changes: ChangesResponse) -> bool:
        """Register a new change in the system."""
        try:
            model = ChangesModel(id=changes.id, changes=changes)
            return model.register()
        except Exception as e:
            Log.save(f"Changes not registered. {e}", __file__, Log.error)
            return False

    @staticmethod
    def delete_changes() -> bool:
        """Delete all changes of the system."""
        try:
            status = ChangesModel.reset_changes()
            return status
        except Exception as e:
            Log.save(f"Changes not deleted. {e}", __file__, Log.error)
            return False