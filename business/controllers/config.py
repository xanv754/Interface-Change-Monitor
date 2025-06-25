from constants.types import RoleTypes
from utils.config import Configuration, ConfigModel
from utils.log import log


class ConfigController:
    """Class to manage config controller."""

    @staticmethod
    def get_config() -> ConfigModel | None:
        """Get config."""
        try:
            configuration = Configuration()
            return configuration.system
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Config controller error. Failed to get config. {error}")
            return None
        
    @staticmethod
    def can_assign_permission(role: str) -> bool:
        try:
            configuration = Configuration()
            if role == RoleTypes.ROOT:
                return configuration.system.can_assign.root
            elif role == RoleTypes.ADMIN:
                return configuration.system.can_assign.admin
            elif role == RoleTypes.USER:
                return configuration.system.can_assign.user
            elif role == RoleTypes.SOPORT:
                return configuration.system.can_assign.soport
            else:
                return False
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Config controller error. Failed to get config. {error}")
            return False
        
    @staticmethod
    def can_view_information_global_permission(role: str) -> bool:
        try:
            configuration = Configuration()
            if role == RoleTypes.ROOT:
                return configuration.system.view_information_global.root
            elif role == RoleTypes.ADMIN:
                return configuration.system.view_information_global.admin
            elif role == RoleTypes.USER:
                return configuration.system.view_information_global.user
            elif role == RoleTypes.SOPORT:
                return configuration.system.view_information_global.soport
            else:
                return False
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Config controller error. Failed to get config. {error}")
            return False