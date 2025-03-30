import os
import json
from constants.types import ProfileType
from constants.paths import FilepathConstant
from constants import config
from schemas.config import SettingSchema, UserPermissionSchema, ChangeNotificationSchema
from schemas.json import JSONSettingSchema, JSONChangeNotificacionSchema
from utils.log import LogHandler

class SettingHandler:
    """Handler to realize operations about configuration basic of the system."""

    __instance: "SettingHandler | None" = None
    __filepath: str = FilepathConstant.SETTINGS.value
    __settings: SettingSchema

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, filepath: str | None = None):
        try:
            if not hasattr(self, "__initialized"):
                if filepath: self.__filepath = filepath
                if not self.__check_exist_settings(self.__filepath):
                    status_create = self.__create_setting_file()
                    if not status_create:
                        raise FileNotFoundError("The setting system was not created correctly.")
                    setting = self.__read_settings()
                    self.__create_setting_model(setting)
                    self._initialized = True
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            exit(1)

    def __check_exist_settings(self, filepath: str) -> bool:
        """Check if the configuration file of the system exists."""
        try:
            if not os.path.exists(filepath):
                raise FileNotFoundError("Setting JSON not found")
            return True
        except Exception as e:
            LogHandler(content=f"System setting not obtained. {e}", path=__file__, err=True)
            return False

    def __create_setting_file(self) -> bool:
        """Create an new default setting of the system."""
        try:
            with open(self.__filepath, "w") as file:
                json.dump(config.DEFAULT, file, indent=4)
        except Exception as e:
            LogHandler(content=f"System setting not updated. {e}", path=__file__, err=True)
            return False
        else:
            return True

    def __read_settings(self) -> dict:
        """Read the setting of the system."""
        try:
            with open(self.__filepath, "r") as file:
                data = json.load(file)
            return data
        except Exception as e:
            LogHandler(content=f"System setting not obtained. {e}", path=__file__, err=True)
            exit(1)

    def __create_setting_model(self, setting: dict) -> None:
        """Create object the setting of the system."""
        try:
            canAssign = UserPermissionSchema(
                ROOT=setting[JSONSettingSchema.CAN_ASSING.value][ProfileType.ROOT.value],
                ADMIN=setting[JSONSettingSchema.CAN_ASSING.value][ProfileType.ADMIN.value],
                STANDARD=setting[JSONSettingSchema.CAN_ASSING.value][ProfileType.STANDARD.value],
                SOPORT=setting[JSONSettingSchema.CAN_ASSING.value][ProfileType.SOPORT.value],
            )
            canReceiveAssignment = UserPermissionSchema(
                ROOT=setting[JSONSettingSchema.CAN_RECEIVE_ASSIGNMENT.value][ProfileType.ROOT.value],
                ADMIN=setting[JSONSettingSchema.CAN_RECEIVE_ASSIGNMENT.value][ProfileType.ADMIN.value],
                STANDARD=setting[JSONSettingSchema.CAN_RECEIVE_ASSIGNMENT.value][ProfileType.STANDARD.value],
                SOPORT=setting[JSONSettingSchema.CAN_RECEIVE_ASSIGNMENT.value][ProfileType.SOPORT.value],
            )
            systemInformation = UserPermissionSchema(
                ROOT=setting[JSONSettingSchema.SYSTEM_INFORMATION.value][ProfileType.ROOT.value],
                ADMIN=setting[JSONSettingSchema.SYSTEM_INFORMATION.value][ProfileType.ADMIN.value],
                STANDARD=setting[JSONSettingSchema.SYSTEM_INFORMATION.value][ProfileType.STANDARD.value],
                SOPORT=setting[JSONSettingSchema.SYSTEM_INFORMATION.value][ProfileType.SOPORT.value],
            )
            notificationChanges = ChangeNotificationSchema(
                ifName=setting[JSONSettingSchema.NOTIFICATION_CHANGES.value][JSONChangeNotificacionSchema.IF_NAME.value],
                ifDescr=setting[JSONSettingSchema.NOTIFICATION_CHANGES.value][JSONChangeNotificacionSchema.IF_DESCR.value],
                ifAlias=setting[JSONSettingSchema.NOTIFICATION_CHANGES.value][JSONChangeNotificacionSchema.IF_ALIAS.value],
                ifHighSpeed=setting[JSONSettingSchema.NOTIFICATION_CHANGES.value][JSONChangeNotificacionSchema.IF_HIGHSPEED.value],
                ifOperStatus=setting[JSONSettingSchema.NOTIFICATION_CHANGES.value][JSONChangeNotificacionSchema.IF_OPERSTATUS.value],
                ifAdminStatus=setting[JSONSettingSchema.NOTIFICATION_CHANGES.value][JSONChangeNotificacionSchema.IF_ADMINSTATUS.value]
            )
            self.__settings = SettingSchema(
                canAssign=canAssign,
                canReceiveAssignment=canReceiveAssignment,
                systemInformation=systemInformation,
                notificationChanges=notificationChanges,
            )
        except Exception as e:
            LogHandler(content=f"System setting not obtained of filepath. {e}", path=__file__, err=True)
            exit(1)

    def get_settings(self) -> SettingSchema:
        """Get the setting of the system."""
        return self.__settings

    def get_filepath(self) -> str:
        """Get the path of the file with the setting of the system."""
        return self.__filepath

    def update_settings(self, new_settings: SettingSchema) -> bool:
        """Update the setting of the system."""
        try:
            with open(self.__filepath, "w") as file:
                json.dump(new_settings.model_dump(), file, indent=4)
            return True
        except Exception as e:
            LogHandler(content=f"System setting not updated. {e}", path=__file__, err=True)
            return False

    def reset_settings(self) -> bool:
        """Reset the setting of the system."""
        try:
            if self.__check_exist_settings(self.__filepath):
                os.remove(self.__filepath)
            self.__create_setting_file()
        except Exception as e:
            LogHandler(content=f"System setting not updated. {e}", path=__file__, err=True)
            return False
        else:
            return True
