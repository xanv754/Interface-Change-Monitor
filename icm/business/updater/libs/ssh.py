import paramiko
import threading
import time
from icm.utils import Configuration, log


class SshHandler:
    """Class to manage ssh connection."""

    _instance: "SshHandler | None" = None
    _config: Configuration
    client: paramiko.SSHClient
    _client: list[paramiko.SSHClient]
    _last_used: float
    _lock: threading.Lock
    isConnected: bool = False

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(SshHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._config = Configuration()
            self.isConnected = False
            self._client = []
            self._last_used = 0
            self._lock = threading.Lock()
            self._initialized = True

    def _ssh_jump(self) -> None:
        try:
            credentials = self._config.snmp
            sock: paramiko.Channel | None = None
            jumps: int = len(credentials) - 1
            for i, credential in enumerate(credentials):
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(
                    username=credential.user,
                    password=credential.password,
                    hostname=credential.host,
                    port=credential.port,
                    sock=sock,
                )
                self._client.append(client)
                if i == jumps:
                    break
                transport = client.get_transport()
                if not transport:
                    raise ValueError("The SSH jump transport failed. Transport is None")
                next_credential = credentials[i + 1]
                dest_addr = (next_credential.host, next_credential.port)
                local_addr = ("127.0.0.1", 0)
                sock = transport.open_channel("direct-tcpip", dest_addr, local_addr)
        except Exception as error:
            log.error(f"SSH Connection: Failed SSH jump to connect - {error}")

    def _auto_close(self, timeout=120) -> None:
        if hasattr(self, "_monitor_thread") and self._monitor_thread.is_alive():
            return

        def monitor() -> None:
            while True:
                time.sleep(5)
                with self._lock:
                    if not self.isConnected:
                        break
                    idle_time = time.time() - self._last_used
                    if idle_time > timeout:
                        log.info(
                            f"SSH auto-close triggered after {int(idle_time)}s of inactivity."
                        )
                        self.disconnect()
                        break

    def get_client(self) -> paramiko.SSHClient:
        return self._client[-1]

    def connect(self) -> None:
        try:
            with self._lock:
                if self.isConnected:
                    self._last_used = time.time()
                    return
                if not self._config:
                    raise ValueError("SSH Configuration not set")
                if self._config.localConnection:
                    raise ValueError("The configuration does not allow SSH connections")
                self._ssh_jump()
                self.isConnected = True
                self._last_used = time.time()
            self._auto_close()
        except ValueError as error:
            self.isConnected = False
            log.error(f"SSH Connection - {error}")
        except Exception as error:
            self.isConnected = False
            log.error(f"SSH Connection: Failed to connect to server - {error}")

    def disconnect(self) -> None:
        try:
            if self.isConnected:
                while len(self._client) > 0:
                    client = self._client.pop()
                    client.close()
        except Exception as error:
            log.error(f"SSH Connection: Failed to disconnect from server - {error}")
        else:
            self.isConnected = False
