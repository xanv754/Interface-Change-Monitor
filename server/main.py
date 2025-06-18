import click
import rich
from datetime import datetime
from cli.users import UserCLI
from database.libs.database import Database
from updater.handler import UpdaterHandler
from utils.log import log


@click.group()
def cli():
    """INTERFACE CHANGE MONITOR
    
    System for monitoring interface changes of devices across the entire available network.
    """
    pass


@cli.command(help="Update information of interfaces")
def updater():
    log.info("Updating information of interfaces...")
    rich.print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [gold1]Updating information of interfaces...")
    system = UpdaterHandler()
    status = system.update()
    if status: 
        log.info("Updater finished")
        rich.print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [green3]Updater finished")
    else: 
        log.error("Updater failed")
        rich.print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [red3]Updater failed")


@cli.command(help="Database administrator")
@click.option("--initialize", is_flag=True, help="Create database tables")
@click.option("--drop", is_flag=True, help="Drop database tables with its data")
def database(initialize: bool, drop: bool):
    database = Database()
    if initialize:
        rich.print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [gold1]Creating database tables...")
        status = database.migration()
        if status: 
            rich.print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [green3]Database tables created")
        else: 
            rich.print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [red3]Database tables not created")
    elif drop:
        rich.print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [gold1]Dropping database tables...")
        status = database.rollback()
        if status: 
            rich.print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [green3]Database tables dropped")
        else: 
            rich.print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} [red3]Database tables not dropped")


@cli.command(help="System administrator")
@click.option("--register", is_flag=True, help="Register a new user")
def system(register: bool):
    if register:
        UserCLI.register()


if __name__ == "__main__":
    cli()