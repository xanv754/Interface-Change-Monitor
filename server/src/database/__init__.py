from database.constants.tables import Tables as GTABLES  # Global Tables
from database.schemas.equipment import EquipmentSchemaDB
from database.schemas.interface import InterfaceSchemaDB
from database.schemas.operator import OperatorSchemaDB
from database.schemas.assignment import AssignmentSchemaDB
from database.tables.equipment import TABLE_SCHEMA_EQUIPMENT
from database.tables.interface import TABLE_SCHEMA_INTERFACE
from database.tables.operator import TABLE_SCHEMA_OPERATOR
from database.tables.assignment import TABLE_SCHEMA_ASSIGNMENT
from database.database import PostgresDatabase
from psycopg2 import errors
