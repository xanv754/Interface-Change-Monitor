import rich
import pandas as pd
from os import path
from datetime import datetime, timedelta
from rich.progress import Progress
from multiprocessing import Pool
from controllers.interface import InterfaceController
from database.querys.interface import InterfaceQuery
from controllers.change import ChangeController
from models.interface import InterfaceField
from updater import SshHandler, HostHandler
from utils.operation import OperationData
from utils.log import log


PATH_DEVICES = f"{path.abspath(__file__).split("/updater")[0]}/files/devices.csv"


class UpdaterHandler:
    """Class to manage updater connection."""

    def __init__(self):
        pass

    def _read_devices(self) -> pd.DataFrame:
        """Read devices to update information."""
        try:
            data = pd.read_csv(PATH_DEVICES, sep=",", names=[InterfaceField.IP, InterfaceField.COMMUNITY])
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
            ssh.disconnect()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Updater handler error. Failed to execute SNMP consults. {error}")
            return pd.DataFrame()
        else:
            return df_interfaces
        
    def _compare_information(self, new_interfaces: pd.DataFrame) -> pd.DataFrame:
        """Compare information of interfaces."""
        try:
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            interface_query = InterfaceQuery()
            old_interfaces = interface_query.get_by_date_consult(yesterday)
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
        
    def update_interfaces(self, data: pd.DataFrame) -> bool:
        """Update information of interfaces in database."""
        try:
            if data.empty: log.info("No interfaces to update")
            else:
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
            date_consult = datetime.now().strftime("%Y-%m-%d")
            df_interfaces = self._execute_consults()
            df_interfaces[InterfaceField.CONSULTED_AT] = date_consult
            if not df_interfaces.empty:
                if self.update_interfaces(df_interfaces):
                    interface_query = InterfaceQuery()
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
            today = datetime.now().strftime("%Y-%m-%d")
            interface_query = InterfaceQuery()
            new_interfaces = interface_query.get_by_date_consult(today)
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