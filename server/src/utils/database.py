import psycopg2
from os import getenv
from dotenv import load_dotenv

load_dotenv(override=True)

URI = getenv("URI")


class PostgresDatabase:
    _connection: psycopg2.extensions.connection
    _cursor: psycopg2.extensions.cursor

    def __init__(self):
        self._connection = psycopg2.connect(URI)
        self._cursor = self._connection.cursor()

    def get_connection(self) -> psycopg2.extensions.connection:
        return self._connection

    def get_cursor(self) -> psycopg2.extensions.cursor:
        return self._cursor

    def close_connection(self) -> None:
        if self._cursor:
            self._cursor.close()
        if self._connection:
            self._connection.close()
