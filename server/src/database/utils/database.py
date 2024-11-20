from os import getenv
from dotenv import load_dotenv
import psycopg2

load_dotenv()

URI = getenv('DATABASE_URL')

class Database:
    __conn: psycopg2.extensions.connection
    __cur: psycopg2.extensions.cursor

    def __init__(self):
        self.open_connection()

    def open_connection(self):
        self.__conn = psycopg2.connect(URI)
        self.__cur = self.__conn.cursor()

    def get_connection(self):
        return self.__conn
    
    def get_cursor(self):
        return self.__cur
    
    def close_connection(self):
        self.__cur.close()
        self.__conn.close()
    