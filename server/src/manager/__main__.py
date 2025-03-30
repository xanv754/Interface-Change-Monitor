import click
from datetime import datetime
from manager.snmp import SNMPHandler
from manager.maintenance import MaintenanceHandler
from manager.setting import SettingHandler
from utils.changes import ChangeDetector
from utils.log import LogHandler


@click.command()
@click.option("--register", is_flag=True, help="Register new operator")
@click.option("--configuration", is_flag=True, help="Export an new configuration file of the system")
@click.option("--reset", is_flag=True, help="Reset the configuration of the system")
@click.option("--update", is_flag=True, help="Load all consults from today")
@click.option("--changes", is_flag=True, help="Detect changes to interface data in the database")
def main(register, configuration, reset, update, changes):
    if register:
        MaintenanceHandler.create_new_operator()
    elif configuration:
        SettingHandler()
        LogHandler(content="The default settings of the system has been created", info=True)
    elif reset:
        status = SettingHandler().reset_settings()
        if status:
            LogHandler(content="The configuration of the system has been reset", info=True)
        else:
            LogHandler(content="The configuration of the system has not been reset", err=True)
    elif update:
        LogHandler(content="Loading data from the last SNMP queries obtained...", warning=True)
        controller = SNMPHandler()
        status = controller.get_consults()
        if status:
            LogHandler(content="Uploaded data", info=True)
        else:
            LogHandler(content="Process of loading data finished, but failed to upload all data", err=True)
    elif changes:
        LogHandler(content="Detecting changes...", warning=True)
        controller = ChangeDetector()
        status = controller.inspect_interfaces()
        if status == 0:
            LogHandler(content="Detector of changes finished. No changes detected", info=True)
        elif status == 1:
            LogHandler(content="Detector of changes finished. Changes detected", info=True)
        elif status == 2:
            LogHandler(content="Detector of changes finished. Failed to registe some changes", warning=True)
        elif status == 3:
            LogHandler(content="Force process of detecting changes", err=True)


if __name__ == "__main__":
    main()
