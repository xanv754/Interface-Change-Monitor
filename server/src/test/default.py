from database import (
    GTABLES,
    EquipmentSchemaDB,
    InterfaceSchemaDB,
    OperatorSchemaDB,
    AssignmentSchemaDB,
    PostgresDatabase
)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""This is the values that will be used for the tests"""

IP = "192.168.1.1"
COMMUNITY = "public"
SYSNAME = "Router1"
IFINDEX = 206
DATE_CONSULT = "2024-01-01"
USERNAME = "user"
PASSWORD = "secret123456"
PASSWORD_HASH = pwd_context.hash(PASSWORD)


def clean_table_equipment() -> None:
    database = PostgresDatabase()
    connection = database.get_connection()
    cursor = database.get_cursor()
    cursor.execute(f"DELETE FROM {GTABLES.EQUIPMENT.value};")
    connection.commit()
    database.close_connection()


def register_equipment() -> int:
    clean_table_equipment()
    database = PostgresDatabase()
    connection = database.get_connection()
    cursor = database.get_cursor()
    cursor.execute(
        f"""
        INSERT INTO {GTABLES.EQUIPMENT.value} (
            {EquipmentSchemaDB.IP.value}, 
            {EquipmentSchemaDB.COMMUNITY.value}, 
            {EquipmentSchemaDB.SYSNAME.value}
        ) VALUES (%s, %s, %s)
        """,
        (IP, COMMUNITY, SYSNAME),
    )
    connection.commit()
    cursor.execute(
        f"""
        SELECT * FROM {GTABLES.EQUIPMENT.value} 
        WHERE {EquipmentSchemaDB.IP.value} = %s AND 
        {EquipmentSchemaDB.COMMUNITY.value} = %s
    """,
        (IP, COMMUNITY),
    )
    result = cursor.fetchone()
    database.close_connection()
    return result[0]


def clean_table_interface() -> None:
    database = PostgresDatabase()
    connection = database.get_connection()
    cursor = database.get_cursor()
    cursor.execute(f"DELETE FROM {GTABLES.INTERFACE.value};")
    connection.commit()
    database.close_connection()


def register_interface(
    clean: bool = True,
    id_equipment: int | None = None,
    date_consult: str | None = None,
    interface_type: str = "NEW",
) -> tuple[int, int]:
    if clean:
        clean_table_interface()
    if id_equipment is None:
        id_equipment = register_equipment()
    if date_consult is None:
        date_consult = DATE_CONSULT
    database = PostgresDatabase()
    connection = database.get_connection()
    cursor = database.get_cursor()
    cursor.execute(
        f"""
        INSERT INTO {GTABLES.INTERFACE.value} (
            {InterfaceSchemaDB.IFINDEX.value}, 
            {InterfaceSchemaDB.ID_EQUIPMENT.value}, 
            {InterfaceSchemaDB.DATE_CONSULT.value}, 
            {InterfaceSchemaDB.INTERFACE_TYPE.value},
            {InterfaceSchemaDB.IFNAME.value}, 
            {InterfaceSchemaDB.IFDESCR.value}, 
            {InterfaceSchemaDB.IFALIAS.value}, 
            {InterfaceSchemaDB.IFSPEED.value}, 
            {InterfaceSchemaDB.IFHIGHSPEED.value}, 
            {InterfaceSchemaDB.IFPHYSADDRESS.value}, 
            {InterfaceSchemaDB.IFTYPE.value}, 
            {InterfaceSchemaDB.IFOPERSTATUS.value}, 
            {InterfaceSchemaDB.IFADMINSTATUS.value}, 
            {InterfaceSchemaDB.IFPROMISCUOUSMODE.value}, 
            {InterfaceSchemaDB.IFCONNECTORPRESENT.value}, 
            {InterfaceSchemaDB.IFLASTCHECK.value}
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)            
        """,
        (
            IFINDEX,
            id_equipment,
            date_consult,
            interface_type,
            "test@ifName",
            "test@ifDescr",
            "test@ifAlias",
            1000,
            1000,
            "test@ifPhysAddress",
            "test@ifType",
            "UP",
            "UP",
            False,
            False,
            "2022-01-01",
        ),
    )
    connection.commit()
    cursor.execute(
        f"""
        SELECT * FROM {GTABLES.INTERFACE.value} 
        WHERE {InterfaceSchemaDB.IFINDEX.value} = %s AND 
        {InterfaceSchemaDB.ID_EQUIPMENT.value} = %s AND 
        {InterfaceSchemaDB.INTERFACE_TYPE.value} = %s
    """,
        (IFINDEX, id_equipment, interface_type),
    )
    result = cursor.fetchone()
    database.close_connection()
    return (id_equipment, result[0])


def clean_table_operator() -> None:
    database = PostgresDatabase()
    connection = database.get_connection()
    cursor = database.get_cursor()
    cursor.execute(f"DELETE FROM {GTABLES.OPERATOR.value};")
    connection.commit()
    database.close_connection()


def register_operator(
    clean: bool = True,
    username: str | None = None,
    profile: str = "STANDARD",
    status_account: str = "ACTIVE",
) -> None:
    if clean:
        clean_table_operator()
    if username is None:
        username = USERNAME
    database = PostgresDatabase()
    connection = database.get_connection()
    cursor = database.get_cursor()
    cursor.execute(
        f"""
        INSERT INTO {GTABLES.OPERATOR.value} (
            {OperatorSchemaDB.USERNAME.value}, 
            {OperatorSchemaDB.NAME.value}, 
            {OperatorSchemaDB.LASTNAME.value}, 
            {OperatorSchemaDB.PASSWORD.value}, 
            {OperatorSchemaDB.PROFILE.value}, 
            {OperatorSchemaDB.STATUS_ACCOUNT.value}
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (username, "test", "user", PASSWORD_HASH, profile, status_account),
    )
    connection.commit()
    database.close_connection()


def clean_table_assignment() -> None:
    database = PostgresDatabase()
    connection = database.get_connection()
    cursor = database.get_cursor()
    cursor.execute(f"DELETE FROM {GTABLES.ASSIGNMENT.value};")
    connection.commit()
    database.close_connection()


def register_assignment() -> tuple[int, int, int]:
    clean_table_assignment()
    register_operator()
    ids = register_interface(clean=False, interface_type="OLD")
    id_equipment = ids[0]
    id_interface_one = ids[1]
    id_interface_two = register_interface(
        clean=False, id_equipment=id_equipment, date_consult="2024-01-02"
    )[1]
    database = PostgresDatabase()
    connection = database.get_connection()
    cursor = database.get_cursor()
    cursor.execute(
        f"""
        INSERT INTO {GTABLES.ASSIGNMENT.value} (
            {AssignmentSchemaDB.CHANGE_INTERFACE.value}, 
            {AssignmentSchemaDB.OLD_INTERFACE.value}, 
            {AssignmentSchemaDB.OPERATOR.value}, 
            {AssignmentSchemaDB.DATE_ASSIGNMENT.value}, 
            {AssignmentSchemaDB.STATUS_ASSIGNMENT.value}, 
            {AssignmentSchemaDB.ASSIGNED_BY.value}
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            id_interface_two,
            id_interface_one,
            USERNAME,
            DATE_CONSULT,
            "PENDING",
            USERNAME,
        ),
    )
    connection.commit()
    cursor.execute(
        f"""
        SELECT * FROM {GTABLES.ASSIGNMENT.value} 
        WHERE {AssignmentSchemaDB.CHANGE_INTERFACE.value} = %s AND 
        {AssignmentSchemaDB.OLD_INTERFACE.value} = %s AND 
        {AssignmentSchemaDB.OPERATOR.value} = %s AND 
        {AssignmentSchemaDB.DATE_ASSIGNMENT.value} = %s
    """,
        (id_interface_two, id_interface_one, USERNAME, DATE_CONSULT),
    )
    result = cursor.fetchone()
    database.close_connection()
    return (id_interface_one, id_interface_two, result[0])


def create_consult(one: bool = True) -> list:
    if one:
        consult = [
            IP,
            COMMUNITY,
            "test@sysname",
            IFINDEX,
            "test@ifName",
            "test@ifDescr",
            "test@ifAlias",
            1000,
            1000,
            "test@ifPhysAddress",
            "test@ifType",
            "UP",
            "UP",
            False,
            False,
            "2022-01-01",
        ]
        return consult
    else:
        consult = [
            IP,
            COMMUNITY,
            "test@sysname",
            IFINDEX,
            "test@ifName2",
            "test@ifDescr",
            "test@ifAlias",
            1000,
            1000,
            "test@ifPhysAddress",
            "test@ifType",
            "UP",
            "UP",
            False,
            False,
            "2022-01-01",
        ]
        return consult
