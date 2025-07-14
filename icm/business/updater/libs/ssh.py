import paramiko
from icm.utils import Configuration, log


class SshHandler:
    """Class to manage ssh connection."""
    _instance: "SshHandler | None" = None
    _config: Configuration
    client: paramiko.SSHClient
    isConnected: bool = False

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(SshHandler, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._config = Configuration()
            self.__initialized_client()
            self._initialized = True

    def __initialized_client(self) -> None:
        """Initialize the client of the SSH connection."""
        try:
            new_client = paramiko.SSHClient()
            new_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"SSH handler error. Failed to initialize client. {error}")
            exit(1)
        else:
            self.client = new_client

    def connect(self) -> None:
        """Connect to the SSH server."""
        if not self.isConnected:
            try:
                self.client.connect(
                    hostname=self._config.system.snmp.host,
                    username=self._config.system.snmp.user,
                    password=self._config.system.snmp.password,
                    port=self._config.system.snmp.port
                )
            except Exception as error:
                error = str(error).strip().capitalize()
                log.error(f"SSH handler error. Failed to connect to server. {error}")
            else:
                self.isConnected = True

    def disconnect(self) -> None:
        """Disconnect from the SSH server."""
        if self.isConnected:
            try:
                self.client.close()
            except Exception as error:
                error = str(error).strip().capitalize()
                log.error(f"SSH handler error. Failed to disconnect from server. {error}")
            else:
                self.isConnected = False