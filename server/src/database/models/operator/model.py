from database import PostgresDatabase, GTABLES, OperatorSchemaDB
from utils import Log

class OperatorModel:
    username: str
    name: str
    lastname: str
    password: str
    profile: str
    statusaccount: str

    def __init__(
        self,
        username: str,
        name: str,
        lastname: str,
        password: str,
        profile: str,
        statusaccount: str,
    ):
        self.username = username.lower()
        self.name = name.capitalize()
        self.lastname = lastname.capitalize()
        self.password = password
        self.profile = profile.upper()
        self.statusaccount = statusaccount.upper()

    def register(self) -> bool:
        """Register an new operator in the database. \n
        _Note:_ All the data required by the new user is extracted from the constructor.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""INSERT INTO {GTABLES.OPERATOR.value} (
                    {OperatorSchemaDB.USERNAME.value},
                    {OperatorSchemaDB.NAME.value},
                    {OperatorSchemaDB.LASTNAME.value},
                    {OperatorSchemaDB.PASSWORD.value},
                    {OperatorSchemaDB.PROFILE.value},
                    {OperatorSchemaDB.STATUS_ACCOUNT.value}
                ) VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    self.username,
                    self.name,
                    self.lastname,
                    self.password,
                    self.profile.upper(),
                    self.statusaccount.upper(),
                ),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False
        else:
            if status and status == "INSERT 0 1":
                return True
            else:
                return False

    def update(self) -> bool:
        """Update data of an operator existing in the database. \n
        _Note:_ All the data required by the new user is extracted from the constructor.
        """
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""UPDATE {GTABLES.OPERATOR.value}
                SET {OperatorSchemaDB.NAME.value} = %s,
                {OperatorSchemaDB.LASTNAME.value} = %s,
                {OperatorSchemaDB.PROFILE.value} = %s,
                {OperatorSchemaDB.STATUS_ACCOUNT.value} = %s
                WHERE {OperatorSchemaDB.USERNAME.value} = %s""",
                (
                    self.name,
                    self.lastname,
                    self.profile,
                    self.statusaccount,
                    self.username,
                ),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            Log.save(e, __file__, Log.error)
            return False
        else:
            if status and status == "UPDATE 1":
                return True
            else:
                return False
