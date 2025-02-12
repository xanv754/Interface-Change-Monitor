import click
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
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} —— The migration has been created!")
    elif rollback:
        database.rollback_inserts()
        database.rollback_table()
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} —— The migration has been rollback!")
    elif clean:
        database.rollback_inserts()
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} —— The tables have been cleaned!")
    database.close_connection()


if __name__ == "__main__":
    main()
