import click
from database.libs.database import Database


@click.group()
def cli():
    pass


@cli.command(help="Execute migration database.")
def migration():
    database = Database()
    database.migration()


@cli.command(help="Execute rollback database.")
def rollback():
    database = Database()
    database.rollback()


if __name__ == "__main__":
    cli()