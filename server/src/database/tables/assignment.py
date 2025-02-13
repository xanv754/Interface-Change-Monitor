from constants import StatusAssignmentType
from database import GTABLES, AssignmentSchema, InterfaceSchema, OperatorSchema

TABLE_SCHEMA_ASSIGNMENT = f"""
    CREATE TABLE {GTABLES.ASSIGNMENT.value} (
        {AssignmentSchema.ID.value} SERIAL PRIMARY KEY,
        {AssignmentSchema.CHANGE_INTERFACE.value} SERIAL REFERENCES {GTABLES.INTERFACE.value}({InterfaceSchema.ID.value}) ON DELETE CASCADE,
        {AssignmentSchema.OLD_INTERFACE.value} SERIAL REFERENCES {GTABLES.INTERFACE.value}({InterfaceSchema.ID.value}) ON DELETE CASCADE,
        {AssignmentSchema.OPERATOR.value} VARCHAR(20) REFERENCES {GTABLES.OPERATOR.value}({OperatorSchema.USERNAME.value}) ON DELETE CASCADE,
        {AssignmentSchema.DATE_ASSIGNMENT.value} DATE NOT NULL,
        {AssignmentSchema.STATUS_ASSIGNMENT.value} VARCHAR(100) NOT NULL,
        {AssignmentSchema.ASSIGNED_BY.value} VARCHAR(60) NOT NULL,
        {AssignmentSchema.UPDATED_AT.value} DATE DEFAULT NULL,
        CONSTRAINT new_assignment UNIQUE (
            {AssignmentSchema.CHANGE_INTERFACE.value}, 
            {AssignmentSchema.OLD_INTERFACE.value}, 
            {AssignmentSchema.OPERATOR.value}
        ),
        CONSTRAINT type_status_assignment CHECK (
            {AssignmentSchema.STATUS_ASSIGNMENT.value} IN (
                '{StatusAssignmentType.PENDING.value}', 
                '{StatusAssignmentType.INSPECTED.value}', 
                '{StatusAssignmentType.REDISCOVERED.value}'
            )
        )
    );
"""