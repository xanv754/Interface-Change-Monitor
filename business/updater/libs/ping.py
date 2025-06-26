from paramiko import ChannelFile
from business.updater.libs.ssh import SshHandler
from utils.log import log


class Ping:
    """Class to manage ping connection."""
    host: str
    isAlive: bool = False

    def __init__(self, host: str):
        self.host = host
        self.isAlive = self.execute()
        

    def __lost_package(self, stdout: ChannelFile) -> bool:
        """Check if package is lost."""
        try:
            if stdout.channel.recv_exit_status() == 0:
                response_bytes = stdout.read()
                response_str = response_bytes.decode("utf-8")
                if "1 received, 0% packet loss" in response_str:
                    return False
            return True
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Ping error. Failed to check if package is lost. {error}")
            return True
        
    def execute(self) -> bool:
        """Execute ping command."""
        try:
            ssh = SshHandler()
            ssh.connect()
            client = ssh.client
            _stdin, stdout, _stderr = client.exec_command(f"ping -c 1 -W 2 {self.host}")
            return not self.__lost_package(stdout)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Ping error. Failed to execute ping command. {error}")
            return False