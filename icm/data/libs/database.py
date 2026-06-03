import psycopg2
from psycopg2 import sql
from icm.data.constants.database import TableNames
from icm.data.schemas.assignment import ASSIGNMENT_SCHEMA
from icm.data.schemas.interface import INTERFACE_SCHEMA
from icm.data.schemas.change import CHANGE_SCHEMA
from icm.data.schemas.user import USER_SCHEMA
from icm.utils import Configuration, log


class Database:
    """Class to manage database connection."""

    _uri: str
    _connection: psycopg2.extensions.connection
    _cursor: psycopg2.extensions.cursor
    connected: bool = False

    def __init__(self, uri: str | None = None):
        if not uri:
            uri = self._get_uri()
        self._uri = uri
        self.open_connection()

    def _get_uri(self) -> str:
        """Get uri of database from configuration."""
        configuration = Configuration()
        return configuration.uri_postgres

    def _check_database(self, uri: str) -> bool:
        """Check if the database exists."""
        try:
            name_db = uri.split("/")[-1]
            uri_base = f"postgres://{uri.split('/')[-2]}/postgres"
            connection = psycopg2.connect(uri_base)
            connection.autocommit = True
            cursor = connection.cursor()
            cursor.execute(
                """
                    SELECT
                        1
                    FROM
                        pg_database
                    WHERE
                        datname = %s
                """,
                (name_db,),
            )
            status = cursor.fetchone() is not None
            cursor.close()
            connection.close()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"PostgreSQL database error. Failed to check database.{error}")
            return False
        else:
            return status

    def _create_database(self, uri: str) -> bool:
        """Create the database (if not exists)."""
        try:
            name_db = uri.split("/")[-1].strip()
            uri_base = f"postgres://{uri.split('/')[-2]}/postgres"
            connection = psycopg2.connect(uri_base)
            connection.autocommit = True
            cursor = connection.cursor()
            cursor.execute(
                sql.SQL(
                    """
                        CREATE DATABASE {db}
                    """
                ).format(db=sql.Identifier(name_db))
            )
            cursor.close()
            connection.close()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"PostgreSQL database Error. Failed to create database. {error}")
            return False
        else:
            log.info("Create database successfully.")
            return True

    def open_connection(self) -> None:
        """Open connection to database."""
        try:
            if not self._check_database(self._uri):
                self._create_database(self._uri)
            self._connection = psycopg2.connect(self._uri)
            self._cursor = self._connection.cursor()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(
                f"PostgreSQL database error. Failed to open connection to database. {error}"
            )
        else:
            self.connected = True

    def get_connection(self) -> psycopg2.extensions.connection:
        """Get connection to database."""
        return self._connection

    def get_cursor(self) -> psycopg2.extensions.cursor:
        """Get cursor to database."""
        return self._cursor

    def close_connection(self) -> None:
        """Close connection to database."""
        if self.connected:
            self._cursor.close()
            self._connection.close()
            self.connected = False

    def initialize(self) -> bool:
        """Create all tables of database."""
        try:
            cursor = self._cursor
            cursor.execute(USER_SCHEMA)
            cursor.execute(INTERFACE_SCHEMA)
            cursor.execute(ASSIGNMENT_SCHEMA)
            cursor.execute(CHANGE_SCHEMA)
            self._connection.commit()
            self.close_connection()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"PostgreSQL database error. Failed to migrate database. {error}")
            return False
        else:
            log.info("Migration database successfully.")
            return True

    def drop(self) -> None:
        """Drop data and tables of database."""
        try:
            cursor = self._cursor
            cursor.execute(f"DROP TABLE IF EXISTS {TableNames.CHANGES}")
            cursor.execute(f"DROP TABLE IF EXISTS {TableNames.ASSIGNMENTS}")
            cursor.execute(f"DROP TABLE IF EXISTS {TableNames.USERS}")
            cursor.execute(f"DROP TABLE IF EXISTS {TableNames.INTERFACES}")
            self._connection.commit()
            self.close_connection()
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(
                f"PostgreSQL database error. Failed to rollback database. {error}"
            )
            return False
        else:
            log.info("Rollback database successfully.")
            return True

