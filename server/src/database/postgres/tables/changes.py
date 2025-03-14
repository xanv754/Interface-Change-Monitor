"""SQL script to create the assignment table."""

from constants import StatusAssignmentType
from database import GTABLES, AssignmentSchemaDB, InterfaceSchemaDB, OperatorSchemaDB, ChangesSchemaDB


TABLE_SCHEMA_ASSIGNMENT = f"""
    CREATE TABLE {GTABLES.ASSIGNMENT.value} (
        {ChangesSchemaDB.ID.value} SERIAL PRIMARY KEY,
        {ChangesSchemaDB.NEW_INTERFACE.value} SERIAL REFERENCES {GTABLES.INTERFACE.value}({InterfaceSchemaDB.ID.value}) ON DELETE CASCADE,
        {ChangesSchemaDB.OLD_INTERFACE.value} SERIAL REFERENCES {GTABLES.INTERFACE.value}({InterfaceSchemaDB.ID.value}) ON DELETE CASCADE,
        {ChangesSchemaDB.OPERATOR.value} VARCHAR(20) REFERENCES {GTABLES.OPERATOR.value}({OperatorSchemaDB.USERNAME.value}) ON DELETE CASCADE DEFAULT NULL,
        CONSTRAINT new_assignment UNIQUE (
            {ChangesSchemaDB.NEW_INTERFACE.value},
            {ChangesSchemaDB.OLD_INTERFACE.value}
        )
    );
"""
