import click
from updater import consultScan, register_new_operator
from utils import Log


@click.command()
@click.option("--today", is_flag=True, help="Load all consults from today")
@click.option("--register", is_flag=True, help="Register new operator")
def main(today, register):
    if today:
        Log.save("Loading data from today", __file__, Log.warning, console=True)
        consultScan()
        Log.save("Interface consults loaded", __file__, Log.info, console=True)
    elif register:
        register_new_operator()


if __name__ == "__main__":
    main()
