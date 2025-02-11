import click
from database import PostgresDatabase

@click.command()
@click.option('--migration', is_flag=True, help="Create of migrate tables")
@click.option('--rollback', is_flag=True, help="Rollback inserts and tables")
def main(migration, rollback):
    database = PostgresDatabase()
    if migration:
        database.create_tables()
        print("Tables created!")
    if rollback:
        database.rollback_inserts()
        database.rollback_table()
        print("Inserts and tables rollback!")
    database.close_connection()

if __name__ == '__main__':
    main()
