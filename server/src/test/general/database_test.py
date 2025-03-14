import unittest
import psycopg2
import redis
from database import PostgresDatabase, RedisDatabase


class TestPostgresDatabase(unittest.TestCase):
    def test_open_connection(self):
        database = PostgresDatabase()
        connection = database.get_connection()
        self.assertEqual(type(connection), psycopg2.extensions.connection)
        self.assertEqual(connection.closed, 0)

    def test_open_cursor(self):
        database = PostgresDatabase()
        cursor = database.get_cursor()
        self.assertEqual(type(cursor), psycopg2.extensions.cursor)

    def test_close_connection(self):
        database = PostgresDatabase()
        connection = database.get_connection()
        database.close_connection()
        self.assertEqual(connection.closed, 1)

class TestRedisDatabase(unittest.TestCase):
    def test_get_connection(self):
        database = RedisDatabase()
        connection = database.get_connection()
        self.assertEqual(type(connection), redis.Redis)
        self.assertEqual(connection.ping(), True)


if __name__ == "__main__":
    unittest.main()
