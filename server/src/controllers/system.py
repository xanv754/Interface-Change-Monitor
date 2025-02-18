from typing import List
from core import SystemConfig
from models import ChangesModel
from schemas import SystemConfigSchema, ChangesSchema
from utils import Log

class SystemController:
    """Controller of the configuration of the system."""

    @staticmethod
    def get_system_config() -> SystemConfigSchema | None:
        """Get the settings of the system."""
        try:
            system_config = SystemConfig()
            return system_config.get_system_config()
        except Exception as e:
            Log.save(f"System configuration not obtained. {e}", __file__, Log.error)
            return None
        
    @staticmethod
    def update_config(config: SystemConfigSchema) -> bool:
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
    def get_all_changes() -> List[ChangesSchema]:
        """Get all changes of the system."""
        try:
            return ChangesModel.get_all_changes()
        except Exception as e:
            Log.save(f"Changes not obtained. {e}", __file__, Log.error)
            return []
