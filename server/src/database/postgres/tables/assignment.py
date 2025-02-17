"""SQL script to create the assignment table."""

from constants import StatusAssignmentType
from database import GTABLES, AssignmentSchemaDB, InterfaceSchemaDB, OperatorSchemaDB


TABLE_SCHEMA_ASSIGNMENT = f"""
    CREATE TABLE {GTABLES.ASSIGNMENT.value} (
        {AssignmentSchemaDB.ID.value} SERIAL PRIMARY KEY,
        {AssignmentSchemaDB.CHANGE_INTERFACE.value} SERIAL REFERENCES {GTABLES.INTERFACE.value}({InterfaceSchemaDB.ID.value}) ON DELETE CASCADE,
        {AssignmentSchemaDB.OLD_INTERFACE.value} SERIAL REFERENCES {GTABLES.INTERFACE.value}({InterfaceSchemaDB.ID.value}) ON DELETE CASCADE,
        {AssignmentSchemaDB.OPERATOR.value} VARCHAR(20) REFERENCES {GTABLES.OPERATOR.value}({OperatorSchemaDB.USERNAME.value}) ON DELETE CASCADE,
        {AssignmentSchemaDB.DATE_ASSIGNMENT.value} DATE NOT NULL,
        {AssignmentSchemaDB.STATUS_ASSIGNMENT.value} VARCHAR(100) NOT NULL,
        {AssignmentSchemaDB.ASSIGNED_BY.value} VARCHAR(60) NOT NULL,
        {AssignmentSchemaDB.UPDATED_AT.value} DATE DEFAULT NULL,
        CONSTRAINT new_assignment UNIQUE (
            {AssignmentSchemaDB.CHANGE_INTERFACE.value}, 
            {AssignmentSchemaDB.OLD_INTERFACE.value}, 
            {AssignmentSchemaDB.OPERATOR.value}
        ),
        CONSTRAINT type_status_assignment CHECK (
            {AssignmentSchemaDB.STATUS_ASSIGNMENT.value} IN (
                '{StatusAssignmentType.PENDING.value}', 
                '{StatusAssignmentType.INSPECTED.value}', 
                '{StatusAssignmentType.REDISCOVERED.value}'
            )
        )
    );
"""
