from os import getenv
from dotenv import load_dotenv
from libs.connection.database import Database
import psycopg2

load_dotenv(override=True)

URI = getenv('POSTGRES_URI')

class Postgres(Database):
    __connection: psycopg2.extensions.connection
    __cursor: psycopg2.extensions.cursor

    def __init__(self):
        self.__connection = psycopg2.connect(URI)
        self.__cursor = self.__connection.cursor()

    def getDatabase(self) -> psycopg2.extensions.connection:
        return self.__connection

    def closeDatabase(self) -> None:
        self.__connection.close()

    def getCursor(self) -> psycopg2.extensions.cursor:
        return self.__cursor
    
    def commit(self) -> None:
        self.__connection.commit()