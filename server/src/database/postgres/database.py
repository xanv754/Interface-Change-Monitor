import psycopg2
from os import getenv
from dotenv import load_dotenv
from database import (
    GTABLES,
    TABLE_SCHEMA_EQUIPMENT,
    TABLE_SCHEMA_INTERFACE,
    TABLE_SCHEMA_OPERATOR,
    TABLE_SCHEMA_ASSIGNMENT,
    TABLE_SCHEMA_CHANGE
)
from utils import Log

load_dotenv(override=True)

URI = getenv("URI")


class PostgresDatabase:
    """Class to interact with the database."""

    _instance: "PostgresDatabase | None" = None
    _connection: psycopg2.extensions.connection
    _cursor: psycopg2.extensions.cursor

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._connection = psycopg2.connect(URI)
        self._cursor = self._connection.cursor()

    def get_connection(self) -> psycopg2.extensions.connection:
        """Get the connection of the database."""
        return self._connection

    def get_cursor(self) -> psycopg2.extensions.cursor:
        """Get the cursor of the database."""
        return self._cursor

    def close_connection(self) -> None:
        """Close the connection of the database."""
        if self._cursor:
            self._cursor.close()
        if self._connection:
            self._connection.close()

    def check_table_exists(self, table: str) -> bool:
        """Check if a table exists in the database.

        Parameters
        ----------
        table : str
            Name of the table.
        """
        self._cursor.execute(
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
        status = self._cursor.fetchone()[0]
        if status:
            return True
        else:
            return False

    def create_tables(self) -> None:
        """Create all tables of the database."""
        try:
            if not self.check_table_exists(GTABLES.EQUIPMENT.value):
                self._cursor.execute(TABLE_SCHEMA_EQUIPMENT)
                self._connection.commit()
            if not self.check_table_exists(GTABLES.INTERFACE.value):
                self._cursor.execute(TABLE_SCHEMA_INTERFACE)
                self._connection.commit()
            if not self.check_table_exists(GTABLES.OPERATOR.value):
                self._cursor.execute(TABLE_SCHEMA_OPERATOR)
                self._connection.commit()
            if not self.check_table_exists(GTABLES.ASSIGNMENT.value):
                self._cursor.execute(TABLE_SCHEMA_ASSIGNMENT)
                self._connection.commit()
            if not self.check_table_exists(GTABLES.CHANGE.value):
                self._cursor.execute(TABLE_SCHEMA_CHANGE)
                self._connection.commit()
        except Exception as e:
            Log.save(e, __file__, Log.error)

    def rollback_inserts(self) -> None:
        """Rollback all inserts in the database."""
        try:
            if self.check_table_exists(GTABLES.EQUIPMENT.value):
                self._cursor.execute(f"DELETE FROM {GTABLES.EQUIPMENT.value};")
                self._connection.commit()
            if self.check_table_exists(GTABLES.INTERFACE.value):
                self._cursor.execute(f"DELETE FROM {GTABLES.INTERFACE.value};")
                self._connection.commit()
            if self.check_table_exists(GTABLES.OPERATOR.value):
                self._cursor.execute(f"DELETE FROM {GTABLES.OPERATOR.value};")
                self._connection.commit()
            if self.check_table_exists(GTABLES.ASSIGNMENT.value):
                self._cursor.execute(f"DELETE FROM {GTABLES.ASSIGNMENT.value};")
                self._connection.commit()
            if self.check_table_exists(GTABLES.CHANGE.value):
                self._cursor.execute(f"DELETE FROM {GTABLES.CHANGE.value};")
                self._connection.commit()
        except Exception as e:
            Log.save(e, __file__, Log.error)

    def rollback_table(self) -> None:
        """Rollback all tables in the database."""
        try:
            if self.check_table_exists(GTABLES.EQUIPMENT.value):
                self._cursor.execute(f"DROP TABLE {GTABLES.EQUIPMENT.value} CASCADE;")
                self._connection.commit()
            if self.check_table_exists(GTABLES.INTERFACE.value):
                self._cursor.execute(f"DROP TABLE {GTABLES.INTERFACE.value} CASCADE;")
                self._connection.commit()
            if self.check_table_exists(GTABLES.OPERATOR.value):
                self._cursor.execute(f"DROP TABLE {GTABLES.OPERATOR.value} CASCADE;")
                self._connection.commit()
            if self.check_table_exists(GTABLES.ASSIGNMENT.value):
                self._cursor.execute(f"DROP TABLE {GTABLES.ASSIGNMENT.value};")
                self._connection.commit()
            if self.check_table_exists(GTABLES.CHANGE.value):
                self._cursor.execute(f"DROP TABLE {GTABLES.CHANGE.value};")
                self._connection.commit()
        except Exception as e:
            Log.save(e, __file__, Log.error)
