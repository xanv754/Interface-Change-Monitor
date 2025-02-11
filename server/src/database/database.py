import psycopg2
from os import getenv
from dotenv import load_dotenv
from constants import GTABLES

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
                """
                CREATE TABLE equipment (
                    id SERIAL PRIMARY KEY,
                    ip VARCHAR(15) UNIQUE NOT NULL,
                    community VARCHAR(30) UNIQUE NOT NULL,
                    sysname VARCHAR(30) NOT NULL,
                    createdAt DATE DEFAULT NOW(),
                    updatedAt DATE DEFAULT NULL,
                    CONSTRAINT new_equipment UNIQUE (ip, community)
                );
            """
            )
            self._connection.commit()
        if not self.check_table_exists(GTABLES.INTERFACE.value):
            self._cursor.execute(
                """
                CREATE TABLE interface (
                    id SERIAL PRIMARY KEY, 
                    ifIndex INTEGER NOT NULL,
                    idEquipment SERIAL REFERENCES equipment(id) ON DELETE CASCADE,
                    dateConsult DATE NOT NULL,
                    ifName VARCHAR(200) NOT NULL,
                    ifDescr VARCHAR(200) NOT NULL,
                    ifAlias VARCHAR(200) NOT NULL,
                    ifSpeed NUMERIC(11) NOT NULL,
                    ifHighSpeed NUMERIC(11) NOT NULL,
                    ifPhysAddress VARCHAR(18) NOT NULL,
                    ifType VARCHAR(200) NOT NULL,
                    ifOperStatus VARCHAR(15) NOT NULL,
                    ifAdminStatus VARCHAR(15) NOT NULL,
                    ifPromiscuousMode BOOLEAN NOT NULL,
                    ifConnectorPresent BOOLEAN NOT NULL,
                    ifLastCheck VARCHAR(40) NOT NULL,
                    CONSTRAINT new_interface UNIQUE (idEquipment, ifIndex, dateConsult),
                    CONSTRAINT type_status_operator CHECK (ifOperStatus IN ('UP', 'DOWN', 'TESTING', 'DORMANT', 'UNKNOWN', 'NOTPRESENT', 'LOWERLAYERDOWN', 'DEFAULT')),
                    CONSTRAINT type_status_administration CHECK (ifAdminStatus IN ('UP', 'DOWN', 'TESTING', 'DORMANT', 'UNKNOWN', 'NOTPRESENT', 'LOWERLAYERDOWN', 'DEFAULT'))
                );                
            """
            )
            self._connection.commit()
        if not self.check_table_exists(GTABLES.OPERATOR.value):
            self._cursor.execute(
                """
                CREATE TABLE operator (
                    username VARCHAR(20) PRIMARY KEY,
                    name VARCHAR(30) NOT NULL, 
                    lastname VARCHAR(30) NOT NULL,
                    password VARCHAR(64) NOT NULL,
                    profile VARCHAR(10) NOT NULL,
                    statusAccount VARCHAR(8) NOT NULL,
                    createdAt DATE DEFAULT NOW(),
                    CONSTRAINT type_profile CHECK (profile IN ('ROOT', 'ADMIN', 'STANDARD', 'SOPORT')),
                    CONSTRAINT status_account CHECK (statusAccount IN ('ACTIVE', 'INACTIVE', 'DELETED'))
                );   
            """
            )
            self._connection.commit()
        if not self.check_table_exists(GTABLES.ASSIGNMENT.value):
            self._cursor.execute(
                """
                CREATE TABLE assignment (
                    id SERIAL PRIMARY KEY,
                    changeInterface SERIAL REFERENCES interface(id) ON DELETE CASCADE,
                    oldInterface SERIAL REFERENCES interface(id) ON DELETE CASCADE,
                    operator VARCHAR(20) REFERENCES operator(username) ON DELETE CASCADE,
                    dateAssignment DATE NOT NULL,
                    statusAssignment VARCHAR(100) NOT NULL,
                    assignedBy VARCHAR(60) NOT NULL,
                    updatedAt DATE DEFAULT NULL,
                    CONSTRAINT new_assignment UNIQUE (changeInterface, oldInterface, operator),
                    CONSTRAINT type_status_assignment CHECK (statusAssignment IN ('PENDING', 'INSPECTED', 'REDISCOVERED'))
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
            self._cursor.execute(f"DROP TABLE {GTABLES.INTERFACE.value};")
            self._connection.commit()
        if self.check_table_exists(GTABLES.OPERATOR.value):
            self._cursor.execute(f"DROP TABLE {GTABLES.OPERATOR.value};")
            self._connection.commit()
        if self.check_table_exists(GTABLES.ASSIGNMENT.value):
            self._cursor.execute(f"DROP TABLE {GTABLES.ASSIGNMENT.value};")
            self._connection.commit()
