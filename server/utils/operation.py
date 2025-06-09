import pandas as pd
from models.interface import InterfaceField
from utils.config import Configuration
from utils.log import log


class OperationData:
    """Class to manage operation data."""

    @staticmethod
    def compare(old_data: pd.DataFrame, new_data: pd.DataFrame) -> pd.DataFrame:
        """Compare two data frames.
        
        Parameters
        ----------
        old_data : pd.DataFrame
            Old data frame.
        new_data : pd.DataFrame
            New data frame.

        Returns
        -------
        pd.DataFrame
            Data frame with the differences.
        """
        try:
            configuration = Configuration()
            keys = [InterfaceField.IP, InterfaceField.COMMUNITY, InterfaceField.SYSNAME, InterfaceField.IFINDEX]
            merge = pd.merge(old_data, new_data, on=keys, how="inner", suffixes=("_old", "_new"))
            if configuration.system.notification_changes.ifName:
                df_ifName = merge[merge[InterfaceField.IFNAME + "_old"] != merge[InterfaceField.IFNAME + "_new"]]
            else:
                df_ifName = pd.DataFrame()
            if configuration.system.notification_changes.ifDescr:
                df_ifDescr = merge[merge[InterfaceField.IFDESCR + "_old"] != merge[InterfaceField.IFDESCR + "_new"]]
            else:
                df_ifDescr = pd.DataFrame()
            if configuration.system.notification_changes.ifAlias:
                df_ifAlias = merge[merge[InterfaceField.IFALIAS + "_old"] != merge[InterfaceField.IFALIAS + "_new"]]
            else:
                df_ifAlias = pd.DataFrame()
            if configuration.system.notification_changes.ifHighSpeed:
                df_ifHighSpeed = merge[merge[InterfaceField.IFHIGHSPEED + "_old"] != merge[InterfaceField.IFHIGHSPEED + "_new"]]
            else:
                df_ifHighSpeed = pd.DataFrame()
            if configuration.system.notification_changes.ifOperStatus:
                df_ifOperStatus = merge[merge[InterfaceField.IFOPERSTATUS + "_old"] != merge[InterfaceField.IFOPERSTATUS + "_new"]]
            else:
                df_ifOperStatus = pd.DataFrame()
            if configuration.system.notification_changes.ifAdminStatus:
                df_ifAdminStatus = merge[merge[InterfaceField.IFADMINSTATUS + "_old"] != merge[InterfaceField.IFADMINSTATUS + "_new"]]
            else:
                df_ifAdminStatus = pd.DataFrame()

            differences = pd.concat([df_ifName, df_ifDescr], axis=0)
            differences = differences.drop_duplicates()
            differences = pd.concat([differences, df_ifAlias], axis=0)
            differences = differences.drop_duplicates()
            differences = pd.concat([differences, df_ifHighSpeed], axis=0)
            differences = differences.drop_duplicates()
            differences = pd.concat([differences, df_ifOperStatus], axis=0)
            differences = differences.drop_duplicates()
            differences = pd.concat([differences, df_ifAdminStatus], axis=0)
            differences = differences.drop_duplicates()
            return differences
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Operation data error. Failed to compare data frames. {error}")
            return pd.DataFrame()