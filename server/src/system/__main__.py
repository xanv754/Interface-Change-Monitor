import click
import rich
from datetime import datetime
from system import SNMPHandler, MaintenanceHandler
from system import SettingHandler
from utils import Log, ChangeDetector

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
        rich.print(
            f"[bold orange3]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [default] The configuration of the system has been [green1]created[default]!"
        )
    elif reset:
        status = SettingHandler().reset_settings()
        if status:
            rich.print(
                f"[bold orange3]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [default] The configuration of the system has been [green1]reset[default]!"
            )
        else:
            rich.print(
                f"[bold orange3]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [default] The configuration of the system has not been [red3]reset[default]!"
            )
    elif update:
        Log.save("Loading data from today...", __file__, Log.info, console=True)
        controller = SNMPHandler()
        status = controller.get_consults()
        if status:
            Log.save("Process of loading data from today finished", __file__, Log.info, console=True)
        else:
            Log.save("Process of loading data from today finished. Failed to load data", __file__, Log.error, console=True)
    elif changes:
        Log.save("Detecting changes...", __file__, Log.info, console=True)
        controller = ChangeDetector()
        status = controller.inspect_interfaces()
        if status == 0:
            Log.save("Process of detecting changes finished. No changes detected", __file__, Log.info, console=True)
        elif status == 1:
            Log.save("Process of detecting changes finished. Changes detected", __file__, Log.info, console=True)
        elif status == 2:
            Log.save("Process of detecting changes finished. Failed to register some changes", __file__, Log.warning, console=True)
        elif status == 3:
            Log.save("Force process of detecting changes.", __file__, Log.error, console=True)


if __name__ == "__main__":
    main()
