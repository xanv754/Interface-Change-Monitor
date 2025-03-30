from manager.setting import SettingHandler
from schemas.config import SettingSchema
from utils.log import LogHandler

class SystemController:
    """Controller of the configuration of the system."""

    @staticmethod
    def get_system_config() -> SettingSchema | None:
        """Get the settings of the system."""
        try:
            system_config = SettingHandler()
            return system_config.get_settings()
        except Exception as e:
            LogHandler(content=f"System configuration not obtained. {e}", path=__file__, err=True)
            return None

    @staticmethod
    def update_config(config: SettingSchema) -> bool:
        """Update the settings of the system.

        Parameters
        ----------
        config : SystemConfigSchema
            New settings of the system.
        """
        try:
            system_config = SettingHandler()
            return system_config.update_settings(config)
        except Exception as e:
            LogHandler(content=f"System configuration not updated. {e}", path=__file__, err=True)
            return False
