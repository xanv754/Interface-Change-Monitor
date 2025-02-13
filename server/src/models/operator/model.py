from database import PostgresDatabase, GTABLES, OperatorSchema


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
        self.username = username
        self.name = name
        self.lastname = lastname
        self.password = password
        self.profile = profile
        self.statusaccount = statusaccount

    def register(self) -> bool:
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""INSERT INTO {GTABLES.OPERATOR.value} (
                    {OperatorSchema.USERNAME.value}, 
                    {OperatorSchema.NAME.value}, 
                    {OperatorSchema.LASTNAME.value}, 
                    {OperatorSchema.PASSWORD.value}, 
                    {OperatorSchema.PROFILE.value}, 
                    {OperatorSchema.STATUS_ACCOUNT.value}
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
            print(e)
            return False
        else:
            if status and status == "INSERT 0 1":
                return True
            else:
                return False

    def update(self) -> bool:
        try:
            database = PostgresDatabase()
            connection = database.get_connection()
            cursor = database.get_cursor()
            cursor.execute(
                f"""UPDATE {GTABLES.OPERATOR.value} 
                SET {OperatorSchema.NAME.value} = %s, 
                {OperatorSchema.LASTNAME.value} = %s, 
                {OperatorSchema.PASSWORD.value} = %s, 
                {OperatorSchema.PROFILE.value} = %s, 
                {OperatorSchema.STATUS_ACCOUNT.value} = %s 
                WHERE {OperatorSchema.USERNAME.value} = %s""",
                (
                    self.name,
                    self.lastname,
                    self.password,
                    self.profile,
                    self.statusaccount,
                    self.username,
                ),
            )
            connection.commit()
            status = cursor.statusmessage
            database.close_connection()
        except Exception as e:
            print(e)
            return False
        else:
            if status and status == "UPDATE 1":
                return True
            else:
                return False
