import click
from updater import SNMP
from system import DetectChanges
from utils import Log


@click.command()
@click.option("--today", is_flag=True, help="Load all consults from today")
@click.option("--changes", is_flag=True, help="Detect changes to interface data in the database")
def main(today, changes):
    if today:
        Log.save("Loading data from today...", __file__, Log.info, console=True)
        controller = SNMP()
        status = controller.get_consults()
        if status:
            Log.save("Process of loading data from today finished", __file__, Log.info, console=True)
        else:
            Log.save("Process of loading data from today finished. Failed to load data", __file__, Log.error, console=True)
    if changes:
        Log.save("Detecting changes...", __file__, Log.info, console=True)
        controller = DetectChanges()
        status = controller.detect_changes()
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
