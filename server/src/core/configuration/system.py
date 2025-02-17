import json
from os import getcwd, path
from constants import ProfileType, config
from schemas import (
    SystemConfigSchema, 
    SystemConfigUserSchema, 
    SystemConfigNotificationSchema, 
    SystemConfigJson,
    SystemConfigNotificationJson
)
from utils import Log

class SystemConfig:
    """Configuration basic of the system."""

    _instance: "SystemConfig | None" = None
    _status_configuration: bool = True
    filepath: str = getcwd() + "/system.config.json"
    configuration: SystemConfigSchema | None = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, filepath: str | None = None):
        try:
            if filepath: self.filepath = filepath
            if not hasattr(self, "_initialized"):
                if not self._check_exist_system_config(self.filepath):
                    status = self._create_system_config()
                    if not status: self._status_configuration = False
                if self._status_configuration:
                    data = self._read_config()
                    if data: self._get_system_config_to_file(data)
                    self._initialized = True
        except Exception as e:
            Log.save(f"{e}", __file__, Log.error, console=True)
    
    def _check_exist_system_config(self, filepath: str) -> bool:
        """Check if the file with the configuration of the system exists."""
        try:
            if not path.exists(filepath):
                return False
            return True
        except Exception as e:
            Log.save(f"System configuration not obtained. {e}", __file__, Log.error, console=True)
            return False
        
    def _create_system_config(self) -> bool:
        """Create an new default configuration of the system."""
        try:
            with open(self.filepath, "w") as file:
                json.dump(config.DEFAULT, file, indent=4)
        except Exception as e:
            Log.save(f"System configuration not updated. {e}", __file__, Log.error, console=True)
            return False
        else:
            return True
    
    def _read_config(self) -> dict:
        """Read the configuration of the system."""
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            return data
        except Exception as e:
            Log.save(f"System configuration not obtained. {e}", __file__, Log.error, console=True)
            return {}
        
    def _get_system_config_to_file(self, config: dict) -> bool:
        """Create the configuration of the system."""
        try:
            canAssign = SystemConfigUserSchema(
                root=config[SystemConfigJson.CAN_ASSING.value][ProfileType.ROOT.value],
                admin=config[SystemConfigJson.CAN_ASSING.value][ProfileType.ADMIN.value],
                standard=config[SystemConfigJson.CAN_ASSING.value][ProfileType.STANDARD.value],
                soport=config[SystemConfigJson.CAN_ASSING.value][ProfileType.SOPORT.value],
            )
            canReceiveAssignment = SystemConfigUserSchema(
                root=config[SystemConfigJson.CAN_RECEIVE_ASSIGNMENT.value][ProfileType.ROOT.value],
                admin=config[SystemConfigJson.CAN_RECEIVE_ASSIGNMENT.value][ProfileType.ADMIN.value],
                standard=config[SystemConfigJson.CAN_RECEIVE_ASSIGNMENT.value][ProfileType.STANDARD.value],
                soport=config[SystemConfigJson.CAN_RECEIVE_ASSIGNMENT.value][ProfileType.SOPORT.value],
            )
            viewAllStatistics = SystemConfigUserSchema(
                root=config[SystemConfigJson.VIEW_ALL_STATISTICS.value][ProfileType.ROOT.value],
                admin=config[SystemConfigJson.VIEW_ALL_STATISTICS.value][ProfileType.ADMIN.value],
                standard=config[SystemConfigJson.VIEW_ALL_STATISTICS.value][ProfileType.STANDARD.value],
                soport=config[SystemConfigJson.VIEW_ALL_STATISTICS.value][ProfileType.SOPORT.value],
            )
            notificationChanges = SystemConfigNotificationSchema(
                ifName=config[SystemConfigJson.NOTIFICATION_CHANGES.value][SystemConfigNotificationJson.IF_NAME.value],
                ifDescr=config[SystemConfigJson.NOTIFICATION_CHANGES.value][SystemConfigNotificationJson.IF_DESCR.value],
                ifAlias=config[SystemConfigJson.NOTIFICATION_CHANGES.value][SystemConfigNotificationJson.IF_ALIAS.value],
                ifSpeed=config[SystemConfigJson.NOTIFICATION_CHANGES.value][SystemConfigNotificationJson.IF_SPEED.value],
                ifHighSpeed=config[SystemConfigJson.NOTIFICATION_CHANGES.value][SystemConfigNotificationJson.IF_HIGHSPEED.value],
                ifPhysAddress=config[SystemConfigJson.NOTIFICATION_CHANGES.value][SystemConfigNotificationJson.IF_PHYSADDRESS.value],
                ifType=config[SystemConfigJson.NOTIFICATION_CHANGES.value][SystemConfigNotificationJson.IF_TYPE.value],
                ifOperStatus=config[SystemConfigJson.NOTIFICATION_CHANGES.value][SystemConfigNotificationJson.IF_OPERSTATUS.value],
                ifAdminStatus=config[SystemConfigJson.NOTIFICATION_CHANGES.value][SystemConfigNotificationJson.IF_ADMINSTATUS.value],
                ifPromiscuousMode=config[SystemConfigJson.NOTIFICATION_CHANGES.value][SystemConfigNotificationJson.IF_PROMISCUOUSMODE.value],
                ifConnectorPresent=config[SystemConfigJson.NOTIFICATION_CHANGES.value][SystemConfigNotificationJson.IF_CONNECTORPRESENT.value],
                ifLastCheck=config[SystemConfigJson.NOTIFICATION_CHANGES.value][SystemConfigNotificationJson.IF_LASTCHECK.value],
            )
            self.configuration = SystemConfigSchema(
                canAssign=canAssign,
                canReceiveAssignment=canReceiveAssignment,
                viewAllStatistics=viewAllStatistics,
                notificationChanges=notificationChanges,
            )
        except Exception as e:
            Log.save(f"System configuration not obtained. {e}", __file__, Log.error, console=True)
            return False
        else:
            return True
        
    def get_system_config(self) -> SystemConfigSchema:
        """Get the configuration of the system."""
        return self.configuration
    
    def get_filepath_config(self) -> str:
        """Get the path of the file with the configuration of the system."""
        return self.filepath
    
    def update_config(self, config: SystemConfigSchema) -> bool:
        """Update the configuration of the system."""
        try:
            with open(self.filepath, "w") as file:
                json.dump(config, file, indent=4)
            return True
        except Exception as e:
            Log.save(f"System configuration not updated. {e}", __file__, Log.error, console=True)