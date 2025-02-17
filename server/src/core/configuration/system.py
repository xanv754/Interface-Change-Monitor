import json
from os import getcwd
from constants import ProfileType
from schemas import (
    SystemConfigSchema, 
    SystemConfigUserSchema, 
    SystemConfigNotificationSchema, 
    SystemConfigJson,
    SystemConfigNotificationJson
)
from utils import Log

class SystemConfig:
    """Settings basic of the system."""

    _instance: "SystemConfig | None" = None
    filepath: str | None = None
    configuration: SystemConfigSchema | None = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.filepath = getcwd() + "/system.config.json"
            data = self._read_config()
            if data: self._create_system_config(data)
            self._initialized = True

    def get_filepath_config(self) -> str:
        """Get the path of the file with the settings of the system."""
        return self.filepath
    
    def _read_config(self) -> dict:
        """Read the settings of the system."""
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
            return data
        except Exception as e:
            Log.save(f"System configuration not obtained. {e}", __file__, Log.error, console=True)
            return {}
        
    def _create_system_config(self, config: dict) -> bool:
        """Create the settings of the system."""
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
        """Get the settings of the system."""
        return self.configuration
    
    def update_config(self, config: SystemConfigSchema) -> bool:
        """Update the settings of the system."""
        try:
            with open(self.filepath, "w") as file:
                json.dump(config, file, indent=4)
            return True
        except Exception as e:
            Log.save(f"System configuration not updated. {e}", __file__, Log.error, console=True)