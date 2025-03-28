import json
import redis
import psycopg2
from os import getenv
from typing import List
from dotenv import load_dotenv
from constants import InterfaceType
from database import GTABLES, ChangesSchemaDB
from schemas import ChangeInterfaceSchema, ChangeSchema
from utils import ChangeDetector
from test import constants, DefaultEquipment, DefaultInterface, DefaultOperator


load_dotenv(override=True)
URI = getenv("URI_TEST")
URI_REDIS_TEST = getenv("URI_REDIS_TEST")

class DefaultChangesPostgresDB:
    @staticmethod
    def clean_table() -> None:
        """Clean the table of the changes."""
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {GTABLES.CHANGE.value};")
        connection.commit()
        cursor.close()
        connection.close()
        DefaultInterface.clean_table()
        DefaultEquipment.clean_table()
        DefaultOperator.clean_table()

    @staticmethod
    def get_change(id: int) -> ChangeSchema | None:
        """Get the change with the given ID."""
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(
            f"""SELECT * FROM {GTABLES.CHANGE.value}
            {ChangesSchemaDB.ID.value} = %s""",
            (
                id,
            ),
        )
        result = cursor.fetchone()
        if result is None:
            return None
        new_change = ChangeSchema(
            id=result[0],
            newInterface=result[1],
            oldInterface=result[2],
            operator=(result[3] if result[3] != None else None)
        )
        cursor.close()
        connection.close()
        return new_change

    @staticmethod
    def new_insert() -> ChangeSchema | None:
        """Create a new change."""
        DefaultChangesPostgresDB.clean_table()
        equipment = DefaultEquipment.new_insert()
        old_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=equipment,
            date=constants.DATE_CONSULT,
            interface_type=InterfaceType.OLD.value,
            ifIndex=constants.IFINDEX
        )
        new_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=equipment,
            date=constants.DATE_CONSULT_TWO,
            interface_type=InterfaceType.NEW.value,
            ifIndex=constants.IFINDEX,
            ifName=constants.IFNAME_TWO
        )
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(
            f"""INSERT INTO {GTABLES.CHANGE.value} (
                {ChangesSchemaDB.NEW_INTERFACE.value},
                {ChangesSchemaDB.OLD_INTERFACE.value}
            ) VALUES (%s, %s)
            """,
            (
                new_interface.id,
                old_interface.id,
            ),
        )
        connection.commit()
        cursor.execute(
            f"""SELECT * FROM {GTABLES.CHANGE.value}
            WHERE {ChangesSchemaDB.NEW_INTERFACE.value} = %s AND
            {ChangesSchemaDB.OLD_INTERFACE.value} = %s""",
            (
                new_interface.id,
                old_interface.id,
            ),
        )
        result = cursor.fetchone()
        if result is None:
            return None
        new_change = ChangeSchema(
            id=result[0],
            newInterface=result[1],
            oldInterface=result[2],
            operator=(result[3] if result[3] != None else None)
        )
        cursor.close()
        connection.close()
        return new_change
