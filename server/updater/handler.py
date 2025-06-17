from os import path
import pandas as pd
from rich.progress import Progress
from multiprocessing import Pool
from updater import SshHandler, HostHandler
from utils.log import log


PATH_DEVICES = f"{path.abspath(__file__).split("/updater")[0]}/files/devices.csv"


class UpdaterHandler:
    """Class to manage updater connection."""

    def __init__(self):
        pass

    def _read_devices(self) -> pd.DataFrame:
        """Read devices to update information."""
        try:
            data = pd.read_csv(PATH_DEVICES, sep=",", names=["Host", "Community"])
            return data
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Updater handler error. Failed to read devices. {error}")
            return pd.DataFrame()
        
    def _worker(self, row: pd.Series) -> pd.DataFrame:
        """Worker to update information of device."""
        try:
            _index, device = row
            ip = device["Host"]
            community = device["Community"]
            host = HostHandler(ip, community)
            if host.isAlive:
                return host.get_info_interfaces()
            return pd.DataFrame()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Updater handler error. Failed to update device. {error}")
            return pd.DataFrame()
        
    def update(self) -> bool:
        """Update information of devices."""
        try:
            devices = self._read_devices()
            if devices.empty:
                log.warning("No devices to update")
                return True
            ssh = SshHandler()
            df = pd.DataFrame()
            with Progress() as progress:
                task = progress.add_task("Getting data of intefaces", total=len(devices))
                with Pool(processes=10) as pool:
                    for index, response in enumerate(pool.imap_unordered(self._worker, devices.iterrows())):
                        if response.empty: continue
                        if df.empty: df = response
                        else: df = pd.concat([df, response], ignore_index=True)
                        progress.update(task, advance=1)
            ssh.disconnect()
            print(df)
            print(df["Host"].unique())
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Updater handler error. Failed to update devices. {error}")
            return False
        else:
            return True


if __name__ == "__main__":
    system = UpdaterHandler()
    system.update()