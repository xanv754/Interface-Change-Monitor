import pandas as pd
from io import StringIO
from icm.constants import InterfaceField
from icm.utils import log
from icm.business.updater.libs.ssh import SshHandler


class SnmpHandler:
    """Class to manage snmp connection."""
    host: str
    community: str

    def __init__(self, host: str, community: str):
        self.host = host
        self.community = community

    def __get_separator(self, type: str) -> str:
        """Get separator of response."""
        if type == InterfaceField.SYSNAME: return "= STRING:"
        elif type == InterfaceField.IFNAME: return "= STRING:"
        elif type == InterfaceField.IFDESCR: return "= STRING:"
        elif type == InterfaceField.IFALIAS: return "= STRING:"
        elif type == InterfaceField.IFHIGHSPEED: return "= Gauge32:"
        elif type == InterfaceField.IFOPERSTATUS: return "= INTEGER:"
        elif type == InterfaceField.IFADMINSTATUS: return "= INTEGER:"
        else: return "="

    def __transform_response_index(self, response: str) -> pd.DataFrame:
        """Transform response of ifIndex to dataframe."""
        try:
            buffer = StringIO("")
            response = response.split("\n")[0:-1]
            response = [value.split("=")[0].strip() for value in response]
            response = [value.split(".")[1].strip() for value in response]
            for value in response:
                buffer.write(value)
                buffer.write("\n")
            buffer.seek(0)
            df = pd.read_csv(buffer, names=[InterfaceField.IFINDEX])
            df = df.dropna(subset=[InterfaceField.IFINDEX])
            df[InterfaceField.IFINDEX] = df[InterfaceField.IFINDEX].astype(int)
            df[InterfaceField.IP] = self.host
            df[InterfaceField.COMMUNITY] = self.community
            df[InterfaceField.SYSNAME] = self.get_sysname()
            new_sort_columns = [InterfaceField.IP, InterfaceField.COMMUNITY, InterfaceField.SYSNAME, InterfaceField.IFINDEX]
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
            separator = self.__get_separator(type)
            buffer = StringIO("")
            response = response.split("\n")[0:]
            for value in response:
                values = value.split(separator)
                buffer.write(";".join(values))
                buffer.write("\n")
            buffer.seek(0)
            df = pd.read_csv(buffer, sep=";", names=[InterfaceField.IFINDEX, type])
            df[type] = df[type].astype(str)
            df[type] = df[type].str.strip().replace("", "CAMPO VACIO")
            df[type] = df[type].fillna("CAMPO VACIO")
            df[InterfaceField.IFINDEX] = df[InterfaceField.IFINDEX].apply(lambda x: int(x.split(f".")[1]))
            df[InterfaceField.IP] = self.host
            df[InterfaceField.COMMUNITY] = self.community
            df[InterfaceField.SYSNAME] = self.get_sysname()
            new_sort_columns = [InterfaceField.IP, InterfaceField.COMMUNITY, InterfaceField.SYSNAME, InterfaceField.IFINDEX, type]
            df = df.reindex(columns=new_sort_columns)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"SNMP handler error. Failed to transform response to dataframe. {error}")
            return pd.DataFrame()
        else:
            return df

        
    def get_sysname(self) -> str:
        """Get sysname of all interfaces."""
        try:
            ssh = SshHandler()
            ssh.connect()
            client = ssh.client
            _stdin, stdout, _stderr = client.exec_command(
                f"snmpwalk -v 2c -c {self.community} {self.host} sysname"
            )
            if stdout.channel.recv_exit_status() == 0:
                response = stdout.read()
                response = response.decode("utf-8")
                separator = self.__get_separator(InterfaceField.SYSNAME)
                return response.split(separator)[1].strip()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"SNMP handler error. Failed to get sysname. {error}")
            return ""
        
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
                return self.__transform_response_index(response)
            return pd.DataFrame()
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
                return self.__transform_response(response, InterfaceField.IFNAME)
            return pd.DataFrame()
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
                return self.__transform_response(response, InterfaceField.IFDESCR)
            return pd.DataFrame()
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
                return self.__transform_response(response, InterfaceField.IFALIAS)
            return pd.DataFrame()
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
                return self.__transform_response(response, InterfaceField.IFHIGHSPEED)
            return pd.DataFrame()
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
                return self.__transform_response(response, InterfaceField.IFOPERSTATUS)
            return pd.DataFrame()
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
                return self.__transform_response(response, InterfaceField.IFADMINSTATUS)
            return pd.DataFrame()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"SNMP handler error. Failed to get ifAdminStatus. {error}")
            return pd.DataFrame()