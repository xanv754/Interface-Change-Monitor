import pandas as pd
from io import StringIO
from updater import SshHandler
from utils.log import log


HOST_COLUMN = "Host"
COMMUNITY_COLUMN = "Community"
IFINDEX_COLUMN = "ifIndex"


class SnmpHandler:
    """Class to manage snmp connection."""
    host: str
    community: str

    def __init__(self, host: str, community: str):
        self.host = host
        self.community = community

    def __transform_response_index(self, response: str) -> pd.DataFrame:
        """Transform response of ifIndex to dataframe."""
        try:
            buffer = StringIO(response)
            response = response.split("\n")[1:]
            for value in response:
                values = value.split(" ")
                buffer.write(";".join(values))
                buffer.write("\n")
            buffer.seek(0)
            df = pd.read_csv(buffer, sep=";", names=["deleted.1", "deleted.2", "deleted.3", IFINDEX_COLUMN])
            df = df.drop(columns=["deleted.1", "deleted.2", "deleted.3"])
            df = df.dropna(subset=[IFINDEX_COLUMN])
            df[IFINDEX_COLUMN] = df[IFINDEX_COLUMN].astype(int)
            df[HOST_COLUMN] = self.host
            df[COMMUNITY_COLUMN] = self.community
            new_sort_columns = [HOST_COLUMN, COMMUNITY_COLUMN, IFINDEX_COLUMN]
            df = df.reindex(columns=new_sort_columns)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"SNMP handler error. Failed to transform response to dataframe. {error}")
            pd.DataFrame()
        else:
            return df
        
    def __transform_response(self, response: str, type: str) -> pd.DataFrame:
        """Transform response to dataframe."""
        try:
            buffer = StringIO(response)
            response = response.split("\n")[1:]
            for value in response:
                values = value.split(" ")
                buffer.write(";".join(values))
                buffer.write("\n")
            buffer.seek(0)
            df = pd.read_csv(buffer, sep=";", names=[IFINDEX_COLUMN, "deleted.2", "deleted.3", type])
            df = df.drop(columns=["deleted.2", "deleted.3"])
            df = df.dropna(subset=[type])
            df[IFINDEX_COLUMN] = df[IFINDEX_COLUMN].apply(lambda x: int(x.split(f".")[1]))
            df[HOST_COLUMN] = self.host
            df[COMMUNITY_COLUMN] = self.community
            new_sort_columns = [HOST_COLUMN, COMMUNITY_COLUMN, IFINDEX_COLUMN, type]
            df = df.reindex(columns=new_sort_columns)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"SNMP handler error. Failed to transform response to dataframe. {error}")
            return pd.DataFrame()
        else:
            return df

    def get_ifIndex(self) -> pd.DataFrame:
        """Get ifIndex of all interfaces."""
        try:
            ssh = SshHandler()
            ssh.connect()
            client = ssh.client
            _stdin, stdout, _stderr = client.exec_command(
                f"snmpwalk -v 2c -c {self.community} {self.host} ifIndex"
            )
            if stdout.channel.recv_exit_status() == 0:
                response = stdout.read()
                response = response.decode("utf-8")
                return self.__transform_response_index(response, "ifIndex")
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"SNMP handler error. Failed to get ifIndex. {error}")
            return pd.DataFrame()

    def get_ifName(self) -> pd.DataFrame:
        """Get ifName of all interfaces."""
        try:
            ssh = SshHandler()
            ssh.connect()
            client = ssh.client
            _stdin, stdout, _stderr = client.exec_command(
                f"snmpwalk -v 2c -c {self.community} {self.host} ifName"
            )
            if stdout.channel.recv_exit_status() == 0:
                response = stdout.read()
                response = response.decode("utf-8")
                return self.__transform_response(response, "ifName")
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"SNMP handler error. Failed to get ifName. {error}")
            return pd.DataFrame()

    def get_ifDescr(self) -> pd.DataFrame:
        """Get ifDescr of all interfaces."""
        try:
            ssh = SshHandler()
            ssh.connect()
            client = ssh.client
            _stdin, stdout, _stderr = client.exec_command(
                f"snmpwalk -v 2c -c {self.community} {self.host} ifDescr"
            )
            if stdout.channel.recv_exit_status() == 0:
                response = stdout.read()
                response = response.decode("utf-8")
                return self.__transform_response(response, "ifDescr")
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"SNMP handler error. Failed to get ifDescr. {error}")
            return pd.DataFrame()

    def get_ifAlias(self) -> pd.DataFrame:
        """Get ifAlias of all interfaces."""
        try:
            ssh = SshHandler()
            ssh.connect()
            client = ssh.client
            _stdin, stdout, _stderr = client.exec_command(
                f"snmpwalk -v 2c -c {self.community} {self.host} ifAlias"
            )
            if stdout.channel.recv_exit_status() == 0:
                response = stdout.read()
                response = response.decode("utf-8")
                return self.__transform_response(response, "ifAlias")
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"SNMP handler error. Failed to get ifAlias. {error}")
            return pd.DataFrame()

    def get_ifHighSpeed(self) -> pd.DataFrame:
        """Get ifHighSpeed of all interfaces."""
        try:
            ssh = SshHandler()
            ssh.connect()
            client = ssh.client
            _stdin, stdout, _stderr = client.exec_command(
                f"snmpwalk -v 2c -c {self.community} {self.host} ifHighSpeed"
            )
            if stdout.channel.recv_exit_status() == 0:
                response = stdout.read()
                response = response.decode("utf-8")
                return self.__transform_response(response, "ifHighSpeed")
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"SNMP handler error. Failed to get ifHighSpeed. {error}")
            return pd.DataFrame()

    def get_ifOperStatus(self) -> pd.DataFrame:
        """Get ifOperStatus of all interfaces."""
        try:
            ssh = SshHandler()
            ssh.connect()
            client = ssh.client
            _stdin, stdout, _stderr = client.exec_command(
                f"snmpwalk -v 2c -c {self.community} {self.host} ifOperStatus"
            )
            if stdout.channel.recv_exit_status() == 0:
                response = stdout.read()
                response = response.decode("utf-8")
                return self.__transform_response(response, "ifOperStatus")
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"SNMP handler error. Failed to get ifOperStatus. {error}")
            return pd.DataFrame()

    def get_ifAdminStatus(self) -> pd.DataFrame:
        """Get ifAdminStatus of all interfaces."""
        try:
            ssh = SshHandler()
            ssh.connect()
            client = ssh.client
            _stdin, stdout, _stderr = client.exec_command(
                f"snmpwalk -v 2c -c {self.community} {self.host} ifAdminStatus"
            )
            if stdout.channel.recv_exit_status() == 0:
                response = stdout.read()
                response = response.decode("utf-8")
                return self.__transform_response(response, "ifAdminStatus")
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"SNMP handler error. Failed to get ifAdminStatus. {error}")
            return pd.DataFrame()