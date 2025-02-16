import click
from updater import consultScan
from utils import Log


@click.command()
@click.option("--today", is_flag=True, help="Load all consults from today")
def main(today):
    if today:
        Log.save("Loading data from today", __file__, Log.warning, console=True)
        consultScan()
        Log.save("Interface consults loaded", __file__, Log.info, console=True)


if __name__ == "__main__":
    main()
