from constants import GTABLES
from database import PostgresDatabase
from schemas import AssignmentSchema


class AssignmentModel:
    change_interface: int
    old_interface: int
    operator: str
    date_assignment: str
    status_assignment: str
    assigned_by: str

    def __init__(
        self,
        change_interface: int,
        old_interface: int,
        operator: str,
        date_assignment: str,
        status_assignment: str,
        assigned_by: str,
    ):
        self.change_interface = change_interface
        self.old_interface = old_interface
        self.operator = operator
        self.date_assignment = date_assignment
        self.status_assignment = status_assignment
        self.assigned_by = assigned_by

    def register(self) -> bool:
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""
                INSERT INTO {GTABLES.ASSIGNMENT.value} (
                    {AssignmentSchema.CHANGE_INTERFACE.value}, 
                    {AssignmentSchema.OLD_INTERFACE.value}, 
                    {AssignmentSchema.OPERATOR.value}, 
                    {AssignmentSchema.DATE_ASSIGNMENT.value}, 
                    {AssignmentSchema.STATUS_ASSIGNMENT.value}, 
                    {AssignmentSchema.ASSIGNED_BY.value}
                ) VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    self.change_interface,
                    self.old_interface,
                    self.operator,
                    self.date_assignment,
                    self.status_assignment,
                    self.assigned_by,
                ),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            print(e)
            return False
        else:
            if status and status == "INSERT 0 1":
                return True
            else:
                return False
