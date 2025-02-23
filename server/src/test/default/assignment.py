import psycopg2
from os import getenv
from dotenv import load_dotenv
from database import GTABLES, AssignmentSchemaDB
from schemas import AssignmentResponseSchema
from test import constants, DefaultInterface, DefaultOperator, DefaultEquipment

load_dotenv(override=True)

URI = getenv("URI_TEST")

class DefaultAssignment:
    @staticmethod
    def clean_table() -> None:
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {GTABLES.ASSIGNMENT.value};")
        cursor.execute(f"DELETE FROM {GTABLES.OPERATOR.value};")
        cursor.execute(f"DELETE FROM {GTABLES.INTERFACE.value};")
        cursor.execute(f"DELETE FROM {GTABLES.EQUIPMENT.value};")
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def new_insert(
        clean: bool = True, 
        status_assignment: str = "PENDING",
        username_operator: str = constants.USERNAME
    ) -> AssignmentResponseSchema | None:
        if clean: DefaultAssignment.clean_table()
        equipment = DefaultEquipment.new_insert()
        if equipment is None: return None
        operator = DefaultOperator.new_insert(username=username_operator)
        if operator is None: return None
        old_interface = DefaultInterface.new_insert(
            clean=False, 
            interface_type="OLD",
            equipment=equipment
        )
        if old_interface is None: return None
        new_interface = DefaultInterface.new_insert(
            clean=False,
            equipment=equipment,
            date=constants.DATE_CONSULT_TWO,
        )
        if new_interface is None: return None
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(
            f"""INSERT INTO {GTABLES.ASSIGNMENT.value} (
                {AssignmentSchemaDB.CHANGE_INTERFACE.value}, 
                {AssignmentSchemaDB.OLD_INTERFACE.value}, 
                {AssignmentSchemaDB.OPERATOR.value}, 
                {AssignmentSchemaDB.DATE_ASSIGNMENT.value}, 
                {AssignmentSchemaDB.STATUS_ASSIGNMENT.value}, 
                {AssignmentSchemaDB.ASSIGNED_BY.value}
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                new_interface.id,
                old_interface.id,
                operator.username,
                constants.DATE_ALTERNATIVE,
                status_assignment,
                constants.USERNAME_ALTERNATIVE,
            ),
        )
        connection.commit()
        cursor.execute(
            f"""SELECT * FROM {GTABLES.ASSIGNMENT.value} 
            WHERE {AssignmentSchemaDB.CHANGE_INTERFACE.value} = %s AND 
            {AssignmentSchemaDB.OLD_INTERFACE.value} = %s AND 
            {AssignmentSchemaDB.OPERATOR.value} = %s""",
            (  
                new_interface.id, 
                old_interface.id, 
                operator.username
            ),
        )
        result = cursor.fetchone()
        if result is None:
            return None
        assignment = AssignmentResponseSchema(
            id=result[0],
            newInterface=result[1],
            oldInterface=result[2],
            operator=result[3],
            date=result[4].strftime("%Y-%m-%d"),
            status=result[5],
            assignedBy=result[6],
            updatedAt=result[7].strftime("%Y-%m-%d") if result[7] != None else None
        )
        cursor.close()
        connection.close()
        return assignment
    
    @staticmethod
    def select_one_by_id(id: int) -> AssignmentResponseSchema | None:
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(
            f"""SELECT * FROM {GTABLES.ASSIGNMENT.value} 
            WHERE {AssignmentSchemaDB.ID.value} = %s""",
            (id,),
        )
        result = cursor.fetchone()
        if result is None:
            return None
        assignment = AssignmentResponseSchema(
            id=result[0],
            newInterface=result[1],
            oldInterface=result[2],
            operator=result[3],
            date=result[4].strftime("%Y-%m-%d"),
            status=result[5],
            assignedBy=result[6],
            updatedAt=result[7].strftime("%Y-%m-%d") if result[7] != None else None
        )
        cursor.close()
        connection.close()
        return assignment
    
    @staticmethod
    def select_one_by_data(id_change_interface: int, id_old_interface: int, operator: str) -> AssignmentResponseSchema | None:
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(
            f"""SELECT * FROM {GTABLES.ASSIGNMENT.value} 
            WHERE {AssignmentSchemaDB.CHANGE_INTERFACE.value} = %s AND 
            {AssignmentSchemaDB.OLD_INTERFACE.value} = %s AND 
            {AssignmentSchemaDB.OPERATOR.value} = %s""",
            (  
                id_change_interface, 
                id_old_interface, 
                operator
            ),
        )
        result = cursor.fetchone()
        if result is None:
            return None
        assignment = AssignmentResponseSchema(
            id=result[0],
            newInterface=result[1],
            oldInterface=result[2],
            operator=result[3],
            date=result[4].strftime("%Y-%m-%d"),
            status=result[5],
            assignedBy=result[6],
            updatedAt=result[7].strftime("%Y-%m-%d") if result[7] != None else None
        )
        cursor.close()
        connection.close()
        return assignment