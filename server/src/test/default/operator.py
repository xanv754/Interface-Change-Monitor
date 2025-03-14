import psycopg2
from os import getenv
from dotenv import load_dotenv
from database import GTABLES, OperatorSchemaDB
from schemas import OperatorSchema
from test import constants

load_dotenv(override=True)

URI = getenv("URI_TEST")

class DefaultOperator:
    @staticmethod
    def clean_table() -> None:
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {GTABLES.OPERATOR.value};")
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def new_insert(
        clean: bool = True, 
        username: str = constants.USERNAME, 
        profile: str = "STANDARD", 
        status_account: str = "ACTIVE",
        password: str = constants.PASSWORD_HASH
    ) -> OperatorSchema | None:
        if clean: DefaultOperator.clean_table()
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(
            f"""INSERT INTO {GTABLES.OPERATOR.value} (
                {OperatorSchemaDB.USERNAME.value}, 
                {OperatorSchemaDB.NAME.value}, 
                {OperatorSchemaDB.LASTNAME.value}, 
                {OperatorSchemaDB.PASSWORD.value}, 
                {OperatorSchemaDB.PROFILE.value}, 
                {OperatorSchemaDB.STATUS_ACCOUNT.value}
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                username, 
                "Unit", 
                "Test", 
                password, 
                profile, 
                status_account
            ),
        )
        connection.commit()
        cursor.execute(
            f"""SELECT * FROM {GTABLES.OPERATOR.value} 
            WHERE {OperatorSchemaDB.USERNAME.value} = %s""",
            (username,),
        )
        result = cursor.fetchone()
        if result is None:
            return None
        user = OperatorSchema(
            username=result[0],
            name=result[1],
            lastname=result[2],
            password=result[3],
            profile=result[4],
            account=result[5],
            createdAt=result[6].strftime("%Y-%m-%d"),
        )
        cursor.close()
        connection.close()
        return user
    
    @staticmethod
    def select_one_by_username(username: str) -> OperatorSchema | None:
        connection = psycopg2.connect(URI)
        cursor = connection.cursor()
        cursor.execute(
            f"""SELECT * FROM {GTABLES.OPERATOR.value} 
            WHERE {OperatorSchemaDB.USERNAME.value} = %s""",
            (username,),
        )
        result = cursor.fetchone()
        if result is None:
            return None
        user = OperatorSchema(
            username=result[0],
            name=result[1],
            lastname=result[2],
            password=result[3],
            profile=result[4],
            account=result[5],
            createdAt=result[6].strftime("%Y-%m-%d"),
        )
        cursor.close()
        connection.close()
        return user