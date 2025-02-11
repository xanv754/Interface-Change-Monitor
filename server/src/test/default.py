from constants import GTABLES, EquipmentFields, InterfaceFields, OperatorFields
from database import PostgresDatabase

"""This is the values that will be used for the tests"""

IP = "192.168.1.1"
COMMUNITY = "public"
SYSNAME = "Router1"
IFINDEX = 206
DATE_CONSULT = "2024-01-01"
USERNAME = "user"

def clean_table_equipment():
    database = PostgresDatabase()
    connection = database.get_connection()
    cursor = database.get_cursor()
    cursor.execute(f"DELETE FROM {GTABLES.EQUIPMENT.value};")
    connection.commit()
    database.close_connection()

def default_register_equipment() -> int:
    clean_table_equipment()
    database = PostgresDatabase()
    connection = database.get_connection()
    cursor = database.get_cursor()
    cursor.execute(f"""
        INSERT INTO {GTABLES.EQUIPMENT.value} (
            {EquipmentFields.IP.value}, 
            {EquipmentFields.COMMUNITY.value}, 
            {EquipmentFields.SYSNAME.value}
        ) VALUES (%s, %s, %s)
        """, (IP, COMMUNITY, SYSNAME),
    )
    connection.commit()
    cursor.execute(F"""
        SELECT * FROM {GTABLES.EQUIPMENT.value} 
        WHERE {EquipmentFields.IP.value} = %s AND 
        {EquipmentFields.COMMUNITY.value} = %s
    """, (IP, COMMUNITY))
    result = cursor.fetchone()
    database.close_connection()
    return result[0]

def clean_table_interface():
    database = PostgresDatabase()
    connection = database.get_connection()
    cursor = database.get_cursor()
    cursor.execute(f"DELETE FROM {GTABLES.INTERFACE.value};")
    connection.commit()
    database.close_connection()

def default_register_interface() -> tuple:
    clean_table_interface()
    id_equipment = default_register_equipment()
    database = PostgresDatabase()
    connection = database.get_connection()
    cursor = database.get_cursor()
    cursor.execute(f"""
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
        """, (
            IFINDEX,
            id_equipment,
            DATE_CONSULT,
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
            "2022-01-01"
        ),
    )
    connection.commit()
    cursor.execute(F"""
        SELECT * FROM {GTABLES.INTERFACE.value} 
        WHERE {InterfaceFields.IFINDEX.value} = %s AND 
        {InterfaceFields.ID_EQUIPMENT.value} = %s AND 
        {InterfaceFields.DATE_CONSULT.value} = %s
    """, (IFINDEX, id_equipment, DATE_CONSULT))
    result = cursor.fetchone()
    database.close_connection()
    return (id_equipment, result[0])

def clean_table_operator():
    database = PostgresDatabase()
    connection = database.get_connection()
    cursor = database.get_cursor()
    cursor.execute(f"DELETE FROM {GTABLES.OPERATOR.value};")
    connection.commit()
    database.close_connection()

def default_register_operator(profile: str = "STANDARD", status_account: str = "ACTIVE"):
    clean_table_operator()
    database = PostgresDatabase()
    connection = database.get_connection()
    cursor = database.get_cursor()
    cursor.execute(f"""
        INSERT INTO {GTABLES.OPERATOR.value} (
            {OperatorFields.USERNAME.value}, 
            {OperatorFields.NAME.value}, 
            {OperatorFields.LASTNAME.value}, 
            {OperatorFields.PASSWORD.value}, 
            {OperatorFields.PROFILE.value}, 
            {OperatorFields.STATUS_ACCOUNT.value}
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            USERNAME,
            "test",
            "user",
            "secret123456",
            profile,
            status_account
        ),
    )
    connection.commit()
    database.close_connection()