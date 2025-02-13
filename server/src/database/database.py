import psycopg2
from os import getenv
from dotenv import load_dotenv
from constants import (
    GTABLES,
    StatusType,
    StatusAssignmentType,
    AccountType,
    ProfileType,
    InterfaceType,
)
from schemas import EquipmentSchema, InterfaceSchema, OperatorSchema, AssignmentSchema

load_dotenv(override=True)

URI = getenv("URI")


class PostgresDatabase:
    _instance: "PostgresDatabase | None" = None
    _connection: psycopg2.extensions.connection
    _cursor: psycopg2.extensions.cursor

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._connection = psycopg2.connect(URI)
        self._cursor = self._connection.cursor()

    def get_connection(self) -> psycopg2.extensions.connection:
        return self._connection

    def get_cursor(self) -> psycopg2.extensions.cursor:
        return self._cursor

    def close_connection(self) -> None:
        if self._cursor:
            self._cursor.close()
        if self._connection:
            self._connection.close()

    def check_table_exists(self, table: str) -> bool:
        self._cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_name = %s
            );
        """,
            (table,),
        )
        status = self._cursor.fetchone()[0]
        if status:
            return True
        else:
            return False

    def create_tables(self) -> None:
        if not self.check_table_exists(GTABLES.EQUIPMENT.value):
            self._cursor.execute(
                f"""
                CREATE TABLE {GTABLES.EQUIPMENT.value} (
                    {EquipmentSchema.ID.value} SERIAL PRIMARY KEY,
                    {EquipmentSchema.IP.value} VARCHAR(15) UNIQUE NOT NULL,
                    {EquipmentSchema.COMMUNITY.value} VARCHAR(30) UNIQUE NOT NULL,
                    {EquipmentSchema.SYSNAME.value} VARCHAR(30) NULL,
                    {EquipmentSchema.CREATED_AT.value} DATE DEFAULT NOW(),
                    {EquipmentSchema.UPDATED_AT.value} DATE DEFAULT NULL,
                    CONSTRAINT new_equipment UNIQUE ({EquipmentSchema.IP.value}, {EquipmentSchema.COMMUNITY.value})
                );
            """
            )
            self._connection.commit()
        if not self.check_table_exists(GTABLES.INTERFACE.value):
            self._cursor.execute(
                f"""
                CREATE TABLE {GTABLES.INTERFACE.value} (
                    {InterfaceSchema.ID.value} SERIAL PRIMARY KEY, 
                    {InterfaceSchema.IFINDEX.value} INTEGER NOT NULL,
                    {InterfaceSchema.ID_EQUIPMENT.value} SERIAL REFERENCES {GTABLES.EQUIPMENT.value}({EquipmentSchema.ID.value}) ON DELETE CASCADE,
                    {InterfaceSchema.DATE_CONSULT.value} DATE NOT NULL,
                    {InterfaceSchema.INTERFACE_TYPE.value} VARCHAR(3) NOT NULL,
                    {InterfaceSchema.IFNAME.value} VARCHAR(200) NOT NULL,
                    {InterfaceSchema.IFDESCR.value} VARCHAR(200) NOT NULL,
                    {InterfaceSchema.IFALIAS.value} VARCHAR(200) NOT NULL,
                    {InterfaceSchema.IFSPEED.value} NUMERIC(11) NOT NULL,
                    {InterfaceSchema.IFHIGHSPEED.value} NUMERIC(11) NOT NULL,
                    {InterfaceSchema.IFPHYSADDRESS.value} VARCHAR(18) NOT NULL,
                    {InterfaceSchema.IFTYPE.value} VARCHAR(200) NOT NULL,
                    {InterfaceSchema.IFOPERSTATUS.value} VARCHAR(15) NOT NULL,
                    {InterfaceSchema.IFADMINSTATUS.value} VARCHAR(15) NOT NULL,
                    {InterfaceSchema.IFPROMISCUOUSMODE.value} BOOLEAN NOT NULL,
                    {InterfaceSchema.IFCONNECTORPRESENT.value} BOOLEAN NOT NULL,
                    {InterfaceSchema.IFLASTCHECK.value} VARCHAR(40) NOT NULL,
                    CONSTRAINT new_interface UNIQUE ({InterfaceSchema.ID_EQUIPMENT.value}, {InterfaceSchema.IFINDEX.value}, {InterfaceSchema.INTERFACE_TYPE.value}),
                    CONSTRAINT type_status_operator CHECK ({InterfaceSchema.IFOPERSTATUS.value} IN ('{StatusType.UP.value}', '{StatusType.DOWN.value}', '{StatusType.TESTING.value}', '{StatusType.DORMANT.value}', '{StatusType.UNKNOWN.value}', '{StatusType.NOTPRESENT.value}', '{StatusType.LOWERLAYERDOWN.value}', '{StatusType.DEFAULT.value}')),
                    CONSTRAINT type_status_administration CHECK ({InterfaceSchema.IFADMINSTATUS.value} IN ('{StatusType.UP.value}', '{StatusType.DOWN.value}', '{StatusType.TESTING.value}', '{StatusType.DORMANT.value}', '{StatusType.UNKNOWN.value}', '{StatusType.NOTPRESENT.value}', '{StatusType.LOWERLAYERDOWN.value}', '{StatusType.DEFAULT.value}')),
                    CONSTRAINT type_interface CHECK ({InterfaceSchema.INTERFACE_TYPE.value} IN ('{InterfaceType.NEW.value}', '{InterfaceType.OLD.value}'))
                );                
            """
            )
            self._connection.commit()
        if not self.check_table_exists(GTABLES.OPERATOR.value):
            self._cursor.execute(
                f"""
                CREATE TABLE {GTABLES.OPERATOR.value} (
                    {OperatorSchema.USERNAME.value} VARCHAR(20) PRIMARY KEY,
                    {OperatorSchema.NAME.value} VARCHAR(30) NOT NULL, 
                    {OperatorSchema.LASTNAME.value} VARCHAR(30) NOT NULL,
                    {OperatorSchema.PASSWORD.value} VARCHAR(64) NOT NULL,
                    {OperatorSchema.PROFILE.value} VARCHAR(10) NOT NULL,
                    {OperatorSchema.STATUS_ACCOUNT.value} VARCHAR(8) NOT NULL,
                    {OperatorSchema.CREATED_AT.value} DATE DEFAULT NOW(),
                    CONSTRAINT type_profile CHECK ({OperatorSchema.PROFILE.value} IN ('{ProfileType.ROOT.value}', '{ProfileType.ADMIN.value}', '{ProfileType.STANDARD.value}', '{ProfileType.SOPORT.value}')),
                    CONSTRAINT status_account CHECK ({OperatorSchema.STATUS_ACCOUNT.value} IN ('{AccountType.ACTIVE.value}', '{AccountType.INACTIVE.value}', '{AccountType.DELETED.value}'))
                );   
            """
            )
            self._connection.commit()
        if not self.check_table_exists(GTABLES.ASSIGNMENT.value):
            self._cursor.execute(
                f"""
                CREATE TABLE {GTABLES.ASSIGNMENT.value} (
                    {AssignmentSchema.ID.value} SERIAL PRIMARY KEY,
                    {AssignmentSchema.CHANGE_INTERFACE.value} SERIAL REFERENCES {GTABLES.INTERFACE.value}({InterfaceSchema.ID.value}) ON DELETE CASCADE,
                    {AssignmentSchema.OLD_INTERFACE.value} SERIAL REFERENCES {GTABLES.INTERFACE.value}({InterfaceSchema.ID.value}) ON DELETE CASCADE,
                    {AssignmentSchema.OPERATOR.value} VARCHAR(20) REFERENCES {GTABLES.OPERATOR.value}({OperatorSchema.USERNAME.value}) ON DELETE CASCADE,
                    {AssignmentSchema.DATE_ASSIGNMENT.value} DATE NOT NULL,
                    {AssignmentSchema.STATUS_ASSIGNMENT.value} VARCHAR(100) NOT NULL,
                    {AssignmentSchema.ASSIGNED_BY.value} VARCHAR(60) NOT NULL,
                    {AssignmentSchema.UPDATED_AT.value} DATE DEFAULT NULL,
                    CONSTRAINT new_assignment UNIQUE ({AssignmentSchema.CHANGE_INTERFACE.value}, {AssignmentSchema.OLD_INTERFACE.value}, {AssignmentSchema.OPERATOR.value}),
                    CONSTRAINT type_status_assignment CHECK ({AssignmentSchema.STATUS_ASSIGNMENT.value} IN ('{StatusAssignmentType.PENDING.value}', '{StatusAssignmentType.INSPECTED.value}', '{StatusAssignmentType.REDISCOVERED.value}'))
                );
            """
            )
            self._connection.commit()

    def rollback_inserts(self) -> None:
        if self.check_table_exists(GTABLES.EQUIPMENT.value):
            self._cursor.execute(f"DELETE FROM {GTABLES.EQUIPMENT.value};")
            self._connection.commit()
        if self.check_table_exists(GTABLES.INTERFACE.value):
            self._cursor.execute(f"DELETE FROM {GTABLES.INTERFACE.value};")
            self._connection.commit()
        if self.check_table_exists(GTABLES.OPERATOR.value):
            self._cursor.execute(f"DELETE FROM {GTABLES.OPERATOR.value};")
            self._connection.commit()
        if self.check_table_exists(GTABLES.ASSIGNMENT.value):
            self._cursor.execute(f"DELETE FROM {GTABLES.ASSIGNMENT.value};")
            self._connection.commit()

    def rollback_table(self) -> None:
        if self.check_table_exists(GTABLES.EQUIPMENT.value):
            self._cursor.execute(f"DROP TABLE {GTABLES.EQUIPMENT.value} CASCADE;")
            self._connection.commit()
        if self.check_table_exists(GTABLES.INTERFACE.value):
            self._cursor.execute(f"DROP TABLE {GTABLES.INTERFACE.value} CASCADE;")
            self._connection.commit()
        if self.check_table_exists(GTABLES.OPERATOR.value):
            self._cursor.execute(f"DROP TABLE {GTABLES.OPERATOR.value} CASCADE;")
            self._connection.commit()
        if self.check_table_exists(GTABLES.ASSIGNMENT.value):
            self._cursor.execute(f"DROP TABLE {GTABLES.ASSIGNMENT.value};")
            self._connection.commit()
