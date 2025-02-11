from constants import (
    GTABLES,
    EquipmentFields,
    InterfaceFields,
    OperatorFields,
    AssignmentFields,
)
from database import PostgresDatabase

"""This is the values that will be used for the tests"""

IP = "192.168.1.1"
COMMUNITY = "public"
SYSNAME = "Router1"
IFINDEX = 206
DATE_CONSULT = "2024-01-01"
USERNAME = "user"


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
            {EquipmentFields.IP.value}, 
            {EquipmentFields.COMMUNITY.value}, 
            {EquipmentFields.SYSNAME.value}
        ) VALUES (%s, %s, %s)
        """,
        (IP, COMMUNITY, SYSNAME),
    )
    connection.commit()
    cursor.execute(
        f"""
        SELECT * FROM {GTABLES.EQUIPMENT.value} 
        WHERE {EquipmentFields.IP.value} = %s AND 
        {EquipmentFields.COMMUNITY.value} = %s
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
    clean: bool = True, id_equipment: int | None = None, date_consult: str | None = None
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
            {InterfaceFields.IFINDEX.value}, 
            {InterfaceFields.ID_EQUIPMENT.value}, 
            {InterfaceFields.DATE_CONSULT.value}, 
            {InterfaceFields.IFNAME.value}, 
            {InterfaceFields.IFDESCR.value}, 
            {InterfaceFields.IFALIAS.value}, 
            {InterfaceFields.IFSPEED.value}, 
            {InterfaceFields.IFHIGHSPEED.value}, 
            {InterfaceFields.IFPHYSADDRESS.value}, 
            {InterfaceFields.IFTYPE.value}, 
            {InterfaceFields.IFOPERSTATUS.value}, 
            {InterfaceFields.IFADMINSTATUS.value}, 
            {InterfaceFields.IFPROMISCUOUSMODE.value}, 
            {InterfaceFields.IFCONNECTORPRESENT.value}, 
            {InterfaceFields.IFLASTCHECK.value}
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)            
        """,
        (
            IFINDEX,
            id_equipment,
            date_consult,
            "eth0",
            "eth0",
            "eth0",
            1000,
            1000,
            "00:00:00:00:00:00",
            "ethernet",
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
        WHERE {InterfaceFields.IFINDEX.value} = %s AND 
        {InterfaceFields.ID_EQUIPMENT.value} = %s AND 
        {InterfaceFields.DATE_CONSULT.value} = %s
    """,
        (IFINDEX, id_equipment, DATE_CONSULT),
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
    clean: bool = True, username: str | None = None, profile: str = "STANDARD", status_account: str = "ACTIVE"
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
            {OperatorFields.USERNAME.value}, 
            {OperatorFields.NAME.value}, 
            {OperatorFields.LASTNAME.value}, 
            {OperatorFields.PASSWORD.value}, 
            {OperatorFields.PROFILE.value}, 
            {OperatorFields.STATUS_ACCOUNT.value}
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (username, "test", "user", "secret123456", profile, status_account),
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
    ids = register_interface(clean=False)
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
            {AssignmentFields.CHANGE_INTERFACE.value}, 
            {AssignmentFields.OLD_INTERFACE.value}, 
            {AssignmentFields.OPERATOR.value}, 
            {AssignmentFields.DATE_ASSIGNMENT.value}, 
            {AssignmentFields.STATUS_ASSIGNMENT.value}, 
            {AssignmentFields.ASSIGNED_BY.value}
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            id_interface_one,
            id_interface_two,
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
        WHERE {AssignmentFields.CHANGE_INTERFACE.value} = %s AND 
        {AssignmentFields.OLD_INTERFACE.value} = %s AND 
        {AssignmentFields.OPERATOR.value} = %s AND 
        {AssignmentFields.DATE_ASSIGNMENT.value} = %s
    """,
        (id_interface_one, id_interface_two, USERNAME, DATE_CONSULT),
    )
    result = cursor.fetchone()
    database.close_connection()
    return (id_interface_one, id_interface_two, result[0])
