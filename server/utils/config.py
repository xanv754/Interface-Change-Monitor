import os
import json
from dotenv import load_dotenv, dotenv_values
from models.config import ConfigField, ConfigModel, ConfigUsers, ConfigInterface
from utils.log import log


load_dotenv(override=True)

URI_POSTGRES = "URI_POSTGRES"
SECRET_KEY = "SECRET_KEY"
SYSTEM_FILENAME = "system.json"
CONFIG_SYSTEM_BASE = ConfigModel(
    can_assign=ConfigUsers(
        root=True,
        admin=True,
        user=False,
        soport=False
    ),
    can_receive_assignment=ConfigUsers(
        root=False,
        admin=True,
        user=True,
        soport=False
    ),
    view_information_global=ConfigUsers(
        root=True,
        admin=True,
        user=False,
        soport=True
    ),
    notification_changes=ConfigInterface(
        ifName=True,
        ifDescr=True,
        ifAlias=True,
        ifHighSpeed=True,
        ifOperStatus=False,
        ifAdminStatus=False
    )
)


class Configuration:
    """Class to manage variable of configuration."""
    _instance: "Configuration | None" = None
    uri_postgres: str
    system: ConfigModel
    key: str

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.__read_env()
            self.__read_config_system()


    def __get_base_path(self) -> str:
        """Get base path of project."""
        base_path = os.path.abspath(__file__).split("/utils")[0]
        return base_path

    def __read_env(self):
        """Read environment variables."""
        path = self.__get_base_path()
        try:
            if os.path.exists(f"{path}/.env.development"):
                env = dotenv_values(f"{path}/.env.development")
            elif os.path.exists(f"{path}/.env.production"):
                env = dotenv_values(f"{path}/.env.production")
            elif os.path.exists(f"{path}/.env"):
                env = dotenv_values(f"{path}/.env")
            else:
                raise FileNotFoundError("No .env file found")
        except FileNotFoundError as error:
            log.error(f"Failed system configuration. {error}")
            exit(1)
        try:
            uri_postgres = env.get(URI_POSTGRES)
            if not uri_postgres: raise ValueError(f"{URI_POSTGRES} not found in .env file")
            key = env.get("SECRET_KEY")
            if not key: raise ValueError(f"{SECRET_KEY} not found in .env file")
        except ValueError as error:
            log.error(f"Failed system configuration. {error}")
            exit(1)
        else:
            self.uri_postgres = uri_postgres
            self.key = key
 
    def __create_base_config(self) -> None:
        """Create base configuration."""
        try:
            path = self.__get_base_path()
            if not os.path.exists(f"{path}/{SYSTEM_FILENAME}"):
                with open(f"{path}/{SYSTEM_FILENAME}", "w") as file:
                    json.dump(CONFIG_SYSTEM_BASE.model_dump(), file, indent=4)
        except Exception as error:
            log.error(f"Failed system configuration. {error}")
            exit(1)

    def __read_config_system(self) -> None:
        """Read configuration system."""
        try:
            path = self.__get_base_path()
            if not os.path.exists(f"{path}/{SYSTEM_FILENAME}"): self.__create_base_config()
            with open(f"{path}/{SYSTEM_FILENAME}", "r") as file:
                system = json.load(file)
            self.system = ConfigModel.model_validate(system)          
        except Exception as error:
            log.error(f"Failed system configuration. {error}")
            exit(1)


if __name__ == "__main__":
    configuration = Configuration()
    print(configuration.uri_postgres)
    print(configuration.system)
    