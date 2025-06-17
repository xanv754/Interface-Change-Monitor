import pandas as pd
from updater import Ping, SnmpHandler, HOST_COLUMN, COMMUNITY_COLUMN, SYSNAME_COLUMN,IFINDEX_COLUMN
from utils.log import log


class HostHandler:
    """Class to manage host connection."""
    host: str
    community: str
    isAlive: bool = False

    def __init__(self, host: str, community: str):
        self.host = host
        self.community = community
        ping = Ping(host)
        self.isAlive = ping.isAlive


    def get_ifIndex_interface(self) -> pd.DataFrame:
        """Get ifIndex of all interfaces."""
        try:
            if not self.isAlive:
                raise ConnectionError("Host is not alive")
            snmp = SnmpHandler(self.host, self.community)
            return snmp.get_ifIndex()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Host handler error. Failed to get ifIndex. {error}")
            return pd.DataFrame()
        
    def get_ifName_interface(self) -> pd.DataFrame:
        """Get ifName of all interfaces."""
        try:
            if not self.isAlive:
                raise ConnectionError("Host is not alive")
            snmp = SnmpHandler(self.host, self.community)
            return snmp.get_ifName()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Host handler error. Failed to get ifName. {error}")
            return pd.DataFrame()
        
    def get_ifDescr_interface(self) -> pd.DataFrame:
        """Get ifDescr of all interfaces."""
        try:
            if not self.isAlive:
                raise ConnectionError("Host is not alive")
            snmp = SnmpHandler(self.host, self.community)
            return snmp.get_ifDescr()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Host handler error. Failed to get ifDescr. {error}")
            return pd.DataFrame()
        
    def get_ifAlias_interface(self) -> pd.DataFrame:
        """Get ifAlias of all interfaces."""
        try:
            if not self.isAlive:
                raise ConnectionError("Host is not alive")
            snmp = SnmpHandler(self.host, self.community)
            return snmp.get_ifAlias()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Host handler error. Failed to get ifAlias. {error}")
            return pd.DataFrame()
        
    def get_ifHighSpeed_interface(self) -> pd.DataFrame:
        """Get ifHighSpeed of all interfaces."""
        try:
            if not self.isAlive:
                raise ConnectionError("Host is not alive")
            snmp = SnmpHandler(self.host, self.community)
            return snmp.get_ifHighSpeed()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Host handler error. Failed to get ifHighSpeed. {error}")
            return pd.DataFrame()
        
    def get_ifOperStatus_interface(self) -> pd.DataFrame:
        """Get ifOperStatus of all interfaces."""
        try:
            if not self.isAlive:
                raise ConnectionError("Host is not alive")
            snmp = SnmpHandler(self.host, self.community)
            return snmp.get_ifOperStatus()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Host handler error. Failed to get ifOperStatus. {error}")
            return pd.DataFrame()
        
    def get_ifAdminStatus_interface(self) -> pd.DataFrame:
        """Get ifAdminStatus of all interfaces."""
        try:
            if not self.isAlive:
                raise ConnectionError("Host is not alive")
            snmp = SnmpHandler(self.host, self.community)
            return snmp.get_ifAdminStatus()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Host handler error. Failed to get ifAdminStatus. {error}")
            return pd.DataFrame()
        
    def get_info_interfaces(self) -> pd.DataFrame:
        """Get all interfaces information."""
        try:
            keys_merge = [HOST_COLUMN, COMMUNITY_COLUMN, SYSNAME_COLUMN, IFINDEX_COLUMN]
            if not self.isAlive:
                raise ConnectionError("Host is not alive")
            data_ifIndex = self.get_ifIndex_interface()
            if data_ifIndex.empty:
                raise ValueError("Index of intefaces is empty")            
            data_ifName = self.get_ifName_interface()
            if not data_ifName.empty:
                data_ifIndex = data_ifIndex.merge(data_ifName, on=keys_merge, how="left")
            data_ifDescr = self.get_ifDescr_interface()
            if not data_ifDescr.empty:
                data_ifIndex = data_ifIndex.merge(data_ifDescr, on=keys_merge, how="left")
            data_ifAlias = self.get_ifAlias_interface()
            if not data_ifAlias.empty:
                data_ifIndex = data_ifIndex.merge(data_ifAlias, on=keys_merge, how="left")
            data_ifHighSpeed = self.get_ifHighSpeed_interface()
            if not data_ifHighSpeed.empty:
                data_ifIndex = data_ifIndex.merge(data_ifHighSpeed, on=keys_merge, how="left")
            data_ifOperStatus = self.get_ifOperStatus_interface()
            if not data_ifOperStatus.empty:
                data_ifIndex = data_ifIndex.merge(data_ifOperStatus, on=keys_merge, how="left")
            data_ifAdminStatus = self.get_ifAdminStatus_interface()
            if not data_ifAdminStatus.empty:
                data_ifIndex = data_ifIndex.merge(data_ifAdminStatus, on=keys_merge, how="left")
            return data_ifIndex
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Host handler error. Failed to get all interfaces information. {error}")
            return pd.DataFrame()