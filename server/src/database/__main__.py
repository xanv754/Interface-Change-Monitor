import click
from rich import print
from datetime import datetime
from database import PostgresDatabase


@click.command()
@click.option("--migration", is_flag=True, help="Create of migrate tables")
@click.option("--rollback", is_flag=True, help="Rollback inserts and tables")
@click.option("--clean", is_flag=True, help="Clean tables")
def main(migration, rollback, clean):
    database = PostgresDatabase()
    if migration:
        database.create_tables()
        print(
            f"[bold orange3]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [bold green3]The migration has been [green1]created[bold green3]!"
        )
    elif rollback:
        database.rollback_inserts()
        database.rollback_table()
        print(
            f"[bold orange3]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [bold green3]The migration has been [red3]rollback[bold green3]!"
        )
    elif clean:
        database.rollback_inserts()
        print(
            f"[bold orange3]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [bold green3]The tables have been [gold1]cleaned[bold green3]!"
        )
    database.close_connection()


if __name__ == "__main__":
    main()
