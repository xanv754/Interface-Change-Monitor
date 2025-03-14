from typing import List
from psycopg2 import sql
from database import PostgresDatabase, GTABLES, ChangesSchemaDB
from schemas import ChangesResponse
from utils import Log

class ChangeModel:
    def register(self, changes: List[ChangesResponse]):
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            with cursor:
                query = sql.SQL("""
                    INSERT INTO {table} ({new_interface}, {old_interface})
                    VALUES (%s, %s)
                """).format(
                        table=sql.Identifier(GTABLES.CHANGES.value),
                        new_interface=sql.Identifier(ChangesSchemaDB.NEW_INTERFACE.value),
                        old_interface=sql.Identifier(ChangesSchemaDB.OLD_INTERFACE.value),
                    )
                for new_change in changes:
                    cursor.execute(query, (
                        new_change.newInterface,
                        new_change.oldInterface,
                    ))
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False
        else:
            if status and "INSERT" in status:
                return True
            else:
                return False
