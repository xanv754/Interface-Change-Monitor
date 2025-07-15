import pandas as pd
from os import path, makedirs
from datetime import datetime, timedelta
from multiprocessing import Pool
from rich.progress import Progress
from icm.access import InterfaceQuery
from icm.constants import InterfaceField
from icm.utils import OperationData, log
from icm.business.controllers.interface import InterfaceController
from icm.business.controllers.change import ChangeController
from icm.business.updater.libs.host import HostHandler
from icm.business.updater.libs.ssh import SshHandler


class UpdaterHandler:
    """Class to manage updater connection."""

    def __init__(self):
        pass

    def _export_consults(self, data: pd.DataFrame) -> None:
        """Export data of consults temporary."""
        try:
            root_path = path.abspath(path.join(path.dirname(__file__), "..", "..", ".."))
            tmp_path = path.join(root_path, "data", "tmp")
            makedirs(tmp_path, exist_ok=True)
            date_consult = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            tmp_path = path.join(tmp_path, f"{date_consult}.csv")
            if data.empty: log.info("No consults to be saved")
            else:
                data.to_csv(tmp_path, index=False, sep=";")
                log.info(f"Consults of {date_consult} saved in tmp folder")
            return True
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Updater handler error. Failed to save consults. {error}")

    def _load_tmp(self) -> pd.DataFrame:
        """Load data of consults temporary if exists."""
        try:
            date_consult = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            root_path = path.abspath(path.join(path.dirname(__file__), "..", "..", ".."))
            tmp_path = path.join(root_path, "data", "tmp", f"{date_consult}.csv")
            if not path.exists(tmp_path): return pd.DataFrame()
            data = pd.read_csv(tmp_path, sep=";")
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Updater handler error. Failed to load consults. {error}")
            return pd.DataFrame()
        else:
            return data

    def _read_devices(self) -> pd.DataFrame:
        """Read devices to update information."""
        try:
            root_path = path.abspath(path.join(path.dirname(__file__), "..", "..", ".."))
            devices_path = path.join(root_path, "data", "sources", "devices.csv")
            data = pd.read_csv(devices_path, sep=",", names=[InterfaceField.IP, InterfaceField.COMMUNITY])
            return data
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Updater handler error. Failed to read devices. {error}")
            return pd.DataFrame()
        
    def _worker(self, row: pd.Series) -> pd.DataFrame:
        """Worker to update information of device."""
        try:
            _index, device = row
            ip = device[InterfaceField.IP]
            community = device[InterfaceField.COMMUNITY]
            host = HostHandler(ip, community)
            if host.isAlive:
                return host.get_info_interfaces()
            else:
                log.info(f"{ip} is not alive")
                return pd.DataFrame()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Updater handler error. Failed to update device. {error}")
            return pd.DataFrame()
        
    def _execute_consults(self) -> pd.DataFrame:
        """Execute consults to get new information of interfaces."""
        try:
            df_interfaces = self._load_tmp()
            if not df_interfaces.empty:
                return df_interfaces
            date_consult = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            devices = self._read_devices()
            if devices.empty:
                log.warning("No devices to update")
                return True
            ssh = SshHandler()
            df_interfaces = pd.DataFrame()
            with Progress() as progress:
                task = progress.add_task("Getting data of interfaces", total=len(devices))
                with Pool(processes=10) as pool:
                    for _index, df_response_snmp in enumerate(pool.imap_unordered(self._worker, devices.iterrows())):
                        if df_response_snmp.empty: 
                            progress.update(task, advance=1)
                            continue
                        if df_interfaces.empty: df_interfaces = df_response_snmp
                        else: df_interfaces = pd.concat([df_interfaces, df_response_snmp], ignore_index=True)
                        progress.update(task, advance=1)
            df_interfaces = df_interfaces.drop_duplicates(
                subset=[
                    InterfaceField.IP, 
                    InterfaceField.COMMUNITY, 
                    InterfaceField.SYSNAME, 
                    InterfaceField.IFINDEX
                ]
            )
            df_interfaces[InterfaceField.CONSULTED_AT] = date_consult
            df_interfaces = df_interfaces.reset_index(drop=True)
            ssh.disconnect()
            self._export_consults(data=df_interfaces)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Updater handler error. Failed to execute SNMP consults. {error}")
            return pd.DataFrame()
        else:
            return df_interfaces
        
    def _compare_information(self, new_interfaces: pd.DataFrame) -> pd.DataFrame:
        """Compare information of interfaces."""
        try:
            before_yesterday = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
            interface_query = InterfaceQuery()
            old_interfaces = interface_query.get_by_date_consult(before_yesterday)
            if old_interfaces.empty: 
                log.info("No interfaces to compare")
                return pd.DataFrame()
            changes = OperationData.compare(old_data=old_interfaces, new_data=new_interfaces)
            if not changes.empty: log.info(f"Change in the interfaces found")
            else: log.info("No changes in the interfaces found")
            return changes
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Updater handler error. Failed to compare information of interfaces. {error}")
            return pd.DataFrame()
        
    def _update_changes(self, data: pd.DataFrame) -> bool:
        """Update information of changes in database."""
        try:
            if data.empty: log.info("No changes to update")
            else:
                change_controller = ChangeController()
                status_operation = change_controller.new_interfaces(data)
                if status_operation.status != 201: raise Exception(status_operation.message)
                log.info("Changes updated")
            return True
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Updater handler error. Failed to update changes. {error}")
            return False
        
    def _update_interfaces(self, data: pd.DataFrame) -> bool:
        """Update information of interfaces in database."""
        try:
            if data.empty: log.info("No interfaces to update")
            else:
                yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                InterfaceController.delete_interfaces_by_date_consult(date=yesterday)
                interface_controller = InterfaceController()
                status_operation = interface_controller.new_interfaces(data)
                if status_operation.status != 201: raise Exception(status_operation.message)
                log.info("Interfaces updated")
            return True
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Updater handler error. Failed to update interfaces. {error}")
            return False
        
    def update(self) -> bool:
        """Update information of devices."""
        try:
            df_interfaces = self._execute_consults()
            if not df_interfaces.empty:
                if self._update_interfaces(df_interfaces):
                    interface_query = InterfaceQuery()
                    date_consult = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                    new_interfaces = interface_query.get_by_date_consult(date=date_consult)
                    if not new_interfaces.empty:
                        changes = self._compare_information(new_interfaces=new_interfaces)
                        if not changes.empty and not self._update_changes(data=changes): 
                            log.warning("Interfaces updated but changes not updated")
                    else: log.error("Problems to get new interfaces to compare")
                    return True
            return False
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Updater handler error. Failed to update devices. {error}")
            return False

    def reload_changes(self) -> bool:
        """Reload changes."""
        try:
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            interface_query = InterfaceQuery()
            new_interfaces = interface_query.get_by_date_consult(yesterday)
            if new_interfaces.empty: 
                log.info("No interfaces to reload")
                return True
            changes = self._compare_information(new_interfaces=new_interfaces)
            if not changes.empty and not self._update_changes(data=changes): 
                log.error("Try to reload changes but not updated")
                return False
            return True
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Updater handler error. Failed to reload changes. {error}")
            return False
    