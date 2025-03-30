import click
from datetime import datetime
from database.database import PostgresDatabase
from utils.log import LogHandler

@click.command()
@click.option("--migration", is_flag=True, help="Create of migrate tables")
@click.option("--rollback", is_flag=True, help="Rollback inserts and tables")
@click.option("--clean", is_flag=True, help="Clean tables")
def main(migration, rollback, clean):
    database = PostgresDatabase()
    if migration:
        database.create_tables()
        LogHandler(content="The migration has been created", info=True)
    elif rollback:
        database.rollback_inserts()
        database.rollback_table()
        LogHandler(content="The migration has been rollback", info=True)
    elif clean:
        database.rollback_inserts()
        LogHandler(content="The tables have been cleaned", info=True)
    database.close_connection()


if __name__ == "__main__":
    main()
