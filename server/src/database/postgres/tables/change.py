"""SQL script to create the assignment table."""

from database import GTABLES, InterfaceSchemaDB, OperatorSchemaDB, ChangesSchemaDB


TABLE_SCHEMA_CHANGE = f"""
    CREATE TABLE {GTABLES.CHANGE.value} (
        {ChangesSchemaDB.ID.value} SERIAL PRIMARY KEY,
        {ChangesSchemaDB.NEW_INTERFACE.value} SERIAL REFERENCES {GTABLES.INTERFACE.value}({InterfaceSchemaDB.ID.value}) ON DELETE CASCADE,
        {ChangesSchemaDB.OLD_INTERFACE.value} SERIAL REFERENCES {GTABLES.INTERFACE.value}({InterfaceSchemaDB.ID.value}) ON DELETE CASCADE,
        {ChangesSchemaDB.OPERATOR.value} VARCHAR(20) REFERENCES {GTABLES.OPERATOR.value}({OperatorSchemaDB.USERNAME.value}) ON DELETE CASCADE DEFAULT NULL,
        CONSTRAINT new_change UNIQUE (
            {ChangesSchemaDB.NEW_INTERFACE.value},
            {ChangesSchemaDB.OLD_INTERFACE.value}
        )
    );
"""
