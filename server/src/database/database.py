import psycopg2
from psycopg2 import sql
from os import getenv
from dotenv import load_dotenv
from database.constants.tables import Tables as GTABLES # Global Tables
from database.tables.equipment import TABLE_SCHEMA_EQUIPMENT
from database.tables.interface import TABLE_SCHEMA_INTERFACE
from database.tables.operator import  TABLE_SCHEMA_OPERATOR
from database.tables.assignment import TABLE_SCHEMA_ASSIGNMENT
from database.tables.change import TABLE_SCHEMA_CHANGE
from utils.log import LogHandler


load_dotenv(override=True)
URI = getenv("URI")


class PostgresDatabase:
    """Class to interact with the database."""

    __instance: "PostgresDatabase | None" = None
    __connection: psycopg2.extensions.connection
    __cursor: psycopg2.extensions.cursor
    __uri: str

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, uri: (str | None) = None):
        if uri is None:
            if not URI:
                raise ValueError("URI not found in environment file.")
            uri = URI
        self.__uri = uri
        status = self.check_database_exists()
        if status:
            self.__connection = psycopg2.connect(self.__uri)
            self.__cursor = self.__connection.cursor()
        else:
            create_db_status = self.create_database()
            if create_db_status:
                self.__connection = psycopg2.connect(self.__uri)
                self.__cursor = self.__connection.cursor()
            else:
                LogHandler(content="Database does not exist and cannot be created.", path=__file__, err=True)
                exit(1)

    def get_connection(self) -> psycopg2.extensions.connection:
        """Get the connection of the database."""
        return self.__connection

    def get_cursor(self) -> psycopg2.extensions.cursor:
        """Get the cursor of the database."""
        return self.__cursor

    def close_connection(self) -> None:
        """Close the connection of the database."""
        if self.__cursor:
            self.__cursor.close()
        if self.__connection:
            self.__connection.close()

    def check_database_exists(self) -> bool:
        """Check if the database exists."""
        try:
            name_db = self.__uri.split("/")[-1]
            uri_basic = f"postgres://{self.__uri.split("/")[-2]}/postgres"
            connection = psycopg2.connect(uri_basic)
            connection.autocommit = True
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT 1
                    FROM pg_database
                    WHERE datname = %s
                """,
                (name_db,),
            )
            status = cursor.fetchone() is not None
            cursor.close()
            connection.close()
            return status
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            exit(1)

    def check_table_exists(self, table: str) -> bool:
        """Check if a table exists in the database.

        Parameters
        ----------
        table : str
            Name of the table.
        """
        try:
            self.__cursor.execute(
                """
                    SELECT EXISTS (
                        SELECT 1
                        FROM information_schema.tables
                        WHERE table_schema = 'public'
                        AND table_name = %s
                    );
                """,
                (table,),
            )
            if self.__cursor.fetchone() is None: return False
            fetch = self.__cursor.fetchone()
            if fetch is None: return False
            status = fetch[0]
            if status: return True
            else: return False
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            exit(1)

    def create_database(self) -> bool:
        """Create the database."""
        try:
            name_db = self.__uri.split("/")[-1]
            uri_basic = f"postgres://{self.__uri.split("/")[-2]}/postgres"
            connection = psycopg2.connect(uri_basic)
            connection.autocommit = True
            cursor = connection.cursor()
            cursor.execute(
                sql.SQL("CREATE DATABASE {db}").format(
                    db=sql.Identifier(name_db)
                )
            )
            cursor.close()
            connection.close()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            exit(1)
        else:
            LogHandler(content="Database was created correctly", path=__file__, info=True)
            return True

    def create_tables(self) -> None:
        """Create all tables of the database."""
        try:
            if not self.check_table_exists(GTABLES.EQUIPMENT.value):
                self.__cursor.execute(TABLE_SCHEMA_EQUIPMENT)
                self.__connection.commit()
            if not self.check_table_exists(GTABLES.INTERFACE.value):
                self.__cursor.execute(TABLE_SCHEMA_INTERFACE)
                self.__connection.commit()
            if not self.check_table_exists(GTABLES.OPERATOR.value):
                self.__cursor.execute(TABLE_SCHEMA_OPERATOR)
                self.__connection.commit()
            if not self.check_table_exists(GTABLES.ASSIGNMENT.value):
                self.__cursor.execute(TABLE_SCHEMA_ASSIGNMENT)
                self.__connection.commit()
            if not self.check_table_exists(GTABLES.CHANGE.value):
                self.__cursor.execute(TABLE_SCHEMA_CHANGE)
                self.__connection.commit()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            exit(1)

    def rollback_inserts(self) -> None:
        """Rollback all inserts in the database."""
        try:
            if self.check_table_exists(GTABLES.EQUIPMENT.value):
                self.__cursor.execute(f"DELETE FROM {GTABLES.EQUIPMENT.value};")
                self.__connection.commit()
            if self.check_table_exists(GTABLES.INTERFACE.value):
                self.__cursor.execute(f"DELETE FROM {GTABLES.INTERFACE.value};")
                self.__connection.commit()
            if self.check_table_exists(GTABLES.OPERATOR.value):
                self.__cursor.execute(f"DELETE FROM {GTABLES.OPERATOR.value};")
                self.__connection.commit()
            if self.check_table_exists(GTABLES.ASSIGNMENT.value):
                self.__cursor.execute(f"DELETE FROM {GTABLES.ASSIGNMENT.value};")
                self.__connection.commit()
            if self.check_table_exists(GTABLES.CHANGE.value):
                self.__cursor.execute(f"DELETE FROM {GTABLES.CHANGE.value};")
                self.__connection.commit()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            exit(1)

    def rollback_table(self) -> None:
        """Rollback all tables in the database."""
        try:
            if self.check_table_exists(GTABLES.EQUIPMENT.value):
                self.__cursor.execute(f"DROP TABLE {GTABLES.EQUIPMENT.value} CASCADE;")
                self.__connection.commit()
            if self.check_table_exists(GTABLES.INTERFACE.value):
                self.__cursor.execute(f"DROP TABLE {GTABLES.INTERFACE.value} CASCADE;")
                self.__connection.commit()
            if self.check_table_exists(GTABLES.OPERATOR.value):
                self.__cursor.execute(f"DROP TABLE {GTABLES.OPERATOR.value} CASCADE;")
                self.__connection.commit()
            if self.check_table_exists(GTABLES.ASSIGNMENT.value):
                self.__cursor.execute(f"DROP TABLE {GTABLES.ASSIGNMENT.value};")
                self.__connection.commit()
            if self.check_table_exists(GTABLES.CHANGE.value):
                self.__cursor.execute(f"DROP TABLE {GTABLES.CHANGE.value};")
                self.__connection.commit()
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            exit(1)
