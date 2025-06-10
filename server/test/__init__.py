import os
import random
import psycopg2
from datetime import datetime, timedelta
from dotenv import load_dotenv, dotenv_values
from constants.types import RoleTypes, UserStatusTypes, AssignmentStatusTypes
from database.constants.database import TableNames
from models.user import UserModel, UserField
from models.interface import InterfaceField, InterfaceModel
from models.change import ChangeField, ChangeModel
from models.assignment import AssignmentField, AssignmentCompleteModel


load_dotenv(override=True)


class DabaseTest:
    _instance: "DabaseTest | None" = None
    uri: str
    connection: psycopg2.extensions.connection
    connected: bool = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DabaseTest, cls).__new__(cls)
        return cls._instance

    def __init__(self, uri: str | None = None):
        try:
            if not hasattr(self, "_initialized"):
                self._initialized = True
                if not uri:
                    file_env = os.path.abspath(__file__).split("/test")[0] + "/.env.development"
                    if not os.path.exists(file_env):
                        raise FileNotFoundError("No .env.development file found")
                env = dotenv_values(file_env)
                self.uri = env.get("URI_POSTGRES")
        except Exception as error:
            print(f"Failed unit test. {error}")
            exit(1)

    def open_connection(self) -> psycopg2.extensions.connection:
        try:
            if not self.connected:
                connection = psycopg2.connect(self.uri)
                self.connection = connection
                self.connected = True
            return self.connection
        except Exception as error:
            print(f"Failed unit test. {error}")
            exit(1)

    def close_connection(self) -> None:
        try:
            if self.connected:
                self.connection.close()
                self.connected = False
        except Exception as error:
            print(f"Failed unit test. {error}")
            exit(1)

    def query_execute(self, query: str) -> None:
        try:
            if self.connected:
                cursor = self.connection.cursor()
                cursor.execute(query)
                self.connection.commit()
        except Exception as error:
            print(f"Failed unit test. {error}")
            exit(1)


class UserDBTest:
    database: DabaseTest

    def __init__(self, uri: str | None = None):
        self.database = DabaseTest(uri=uri)

    def get_mock(self) -> UserModel:
        return UserModel(
            username="unittest" + str(random.randint(0, 1000)),
            password="test_password",
            name="Unit" ,
            lastname="Test",
            status=UserStatusTypes.ACTIVE,
            role=RoleTypes.ADMIN,
            created_at=None,
            updated_at=None
        )

    def create_table(self) -> None:
        try:
            self.database.open_connection()
            self.database.query_execute(
                f"""CREATE TABLE IF NOT EXISTS {TableNames.USERS} (
                    {UserField.USERNAME} VARCHAR(20) PRIMARY KEY,
                    {UserField.PASSWORD} VARCHAR(20) NOT NULL,
                    {UserField.NAME} VARCHAR(50) NOT NULL,
                    {UserField.LASTNAME} VARCHAR(50) NOT NULL,
                    {UserField.STATUS} VARCHAR(8) NOT NULL,
                    {UserField.ROLE} VARCHAR(6) NOT NULL,
                    {UserField.CREATED_AT} DATE DEFAULT CURRENT_DATE,
                    {UserField.UPDATED_AT} DATE DEFAULT NULL,
                    CONSTRAINT {TableNames.USERS}_status CHECK ({UserField.STATUS} IN ('{UserStatusTypes.ACTIVE}', '{UserStatusTypes.INACTIVE}', '{UserStatusTypes.DELETED}')),
                    CONSTRAINT {TableNames.USERS}_role CHECK ({UserField.ROLE} IN ('{RoleTypes.ADMIN}', '{RoleTypes.ROOT}', '{RoleTypes.USER}', '{RoleTypes.SOPORT}'))
                )"""
            )
            self.database.close_connection()
        except Exception as error:
            print(f"Failed unit test. Error user database. {error}")
            exit(1)

    def insert(self, new_user: UserModel) -> None:
        try:
            self.database.open_connection()
            self.database.query_execute(
                f"""
                    INSERT INTO {TableNames.USERS} (
                        {UserField.USERNAME},
                        {UserField.PASSWORD},
                        {UserField.NAME},
                        {UserField.LASTNAME},
                        {UserField.STATUS},
                        {UserField.ROLE}
                    ) VALUES (
                        '{new_user.username}',
                        '{new_user.password}',
                        '{new_user.name}',
                        '{new_user.lastname}',
                        '{new_user.status}',
                        '{new_user.role}'
                    )
                """
            )
            self.database.close_connection()
        except Exception as error:
            print(f"Failed unit test. Error user database. {error}")
            exit(1)

    def get(self, username: str) -> UserModel | None:
        try:
            self.database.open_connection()
            cursor = self.database.connection.cursor()
            cursor.execute(
                f"""
                    SELECT
                        *
                    FROM
                        {TableNames.USERS}
                    WHERE
                        {UserField.USERNAME} = %s
                """,
                (username,)
            )
            response = cursor.fetchone()
            self.database.close_connection()
            if response:
                return UserModel(
                    username=response[0],
                    password=response[1],
                    name=response[2],
                    lastname=response[3],
                    status=response[4],
                    role=response[5],
                    created_at=response[6],
                    updated_at=response[7].strftime("%Y-%m-%d") if response[7] else None
                )
            return None
        except Exception as error:
            print(f"Failed unit test. Error user database. {error}")
            exit(1)

    def clean(self) -> None:
        try:
            self.database.open_connection()
            self.database.query_execute(f"DELETE FROM {TableNames.USERS}")
            self.database.close_connection()
        except Exception as error:
            print(f"Failed unit test. Error user database. {error}")
            exit(1)


class InterfaceDBTest:
    database: DabaseTest

    def __init__(self, uri: str | None = None):
        self.database = DabaseTest(uri=uri)

    def get_mock(self, yesterday: bool = False) -> InterfaceModel:
        if yesterday: date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        else: date = datetime.now()
        return InterfaceModel(
            id=None,
            ip=f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
            community="public" + str(random.randint(0, 1000)),
            sysname="sysname" + str(random.randint(0, 1000)),
            ifIndex=random.randint(0, 1000),
            ifName="ifNameTest",
            ifDescr="ifDescrTest",
            ifAlias="ifAliasTest",
            ifHighSpeed=1000,
            ifOperStatus="up",
            ifAdminStatus="up",
            consulted_at=date.strftime("%Y-%m-%d")
        )

    def create_table(self) -> None:
        try:
            self.database.open_connection()
            self.database.query_execute(
                f"""CREATE TABLE IF NOT EXISTS {TableNames.INTERFACES} (
                    {InterfaceField.ID} SERIAL PRIMARY KEY,
                    {InterfaceField.IP} VARCHAR(15) NOT NULL,
                    {InterfaceField.COMMUNITY} VARCHAR(100) NOT NULL,
                    {InterfaceField.SYSNAME} VARCHAR(100) NOT NULL,
                    {InterfaceField.IFINDEX} NUMERIC NOT NULL,
                    {InterfaceField.IFNAME} VARCHAR NOT NULL,
                    {InterfaceField.IFDESCR} VARCHAR NOT NULL,
                    {InterfaceField.IFALIAS} VARCHAR NOT NULL,
                    {InterfaceField.IFHIGHSPEED} NUMERIC NOT NULL,
                    {InterfaceField.IFOPERSTATUS} VARCHAR(100) NOT NULL,
                    {InterfaceField.IFADMINSTATUS} VARCHAR(100) NOT NULL,
                    {InterfaceField.CONSULTED_AT} DATE NOT NULL,
                    CONSTRAINT {TableNames.INTERFACES}_unique UNIQUE (
                        {InterfaceField.IP}, 
                        {InterfaceField.COMMUNITY},
                        {InterfaceField.SYSNAME},
                        {InterfaceField.IFINDEX},
                        {InterfaceField.CONSULTED_AT}
                    )
                )"""
            )
            self.database.close_connection()
        except Exception as error:
            print(f"Failed unit test. Error interface database. {error}")
            exit(1)

    def insert(self, new_interface: InterfaceModel) -> None:
        try:
            self.database.open_connection()
            self.database.query_execute(
                f"""
                    INSERT INTO {TableNames.INTERFACES} (
                        {InterfaceField.IP},
                        {InterfaceField.COMMUNITY},
                        {InterfaceField.SYSNAME},
                        {InterfaceField.IFINDEX},
                        {InterfaceField.IFNAME},
                        {InterfaceField.IFDESCR},
                        {InterfaceField.IFALIAS},
                        {InterfaceField.IFHIGHSPEED},
                        {InterfaceField.IFOPERSTATUS},
                        {InterfaceField.IFADMINSTATUS},
                        {InterfaceField.CONSULTED_AT}
                    ) VALUES (
                        '{new_interface.ip}',
                        '{new_interface.community}',
                        '{new_interface.sysname}',
                        {new_interface.ifIndex},
                        '{new_interface.ifName}',
                        '{new_interface.ifDescr}',
                        '{new_interface.ifAlias}',
                        {new_interface.ifHighSpeed},
                        '{new_interface.ifOperStatus}',
                        '{new_interface.ifAdminStatus}',
                        '{new_interface.consulted_at}'
                    )
                """
            )
            self.database.close_connection()
        except Exception as error:
            print(f"Failed unit test. Error interface database. {error}")
            exit(1)

    def get(self, ip: str, community: str, sysname: str, ifIndex: int, consulted_at: str) -> InterfaceModel | None:
        try:
            self.database.open_connection()
            cursor = self.database.connection.cursor()
            cursor.execute(
                f"""
                    SELECT
                        *
                    FROM
                        {TableNames.INTERFACES}
                    WHERE
                        {InterfaceField.IP} = %s AND
                        {InterfaceField.COMMUNITY} = %s AND
                        {InterfaceField.SYSNAME} = %s AND
                        {InterfaceField.IFINDEX} = %s AND
                        {InterfaceField.CONSULTED_AT} = %s
                """,
                (ip, community, sysname, ifIndex, consulted_at)
            )
            response = cursor.fetchone()
            self.database.close_connection()
            if response:
                return InterfaceModel(
                    id=response[0],
                    ip=response[1],
                    community=response[2],
                    sysname=response[3],
                    ifIndex=response[4],
                    ifName=response[5],
                    ifDescr=response[6],
                    ifAlias=response[7],
                    ifHighSpeed=response[8],
                    ifOperStatus=response[9],
                    ifAdminStatus=response[10],
                    consulted_at=response[11].strftime("%Y-%m-%d") if response[11] else None
                )
            return None
        except Exception as error:
            print(f"Failed unit test. Error interface database. {error}")
            exit(1)

    def clean(self) -> None:
        try:
            self.database.open_connection()
            self.database.query_execute(f"DELETE FROM {TableNames.INTERFACES}")
            self.database.close_connection()
        except Exception as error:
            print(f"Failed unit test. Error interface database. {error}")
            exit(1)


class ChangeDBTest:
    database: DabaseTest
    interface_database: InterfaceDBTest = InterfaceDBTest()
    user_database: UserDBTest = UserDBTest()

    def __init__(self, uri: str | None = None):
        self.database = DabaseTest(uri=uri)

    def get_mock(self) -> ChangeModel:
        ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        community = "public" + str(random.randint(0, 1000))
        sysname = "sysname" + str(random.randint(0, 1000))
        ifIndex = random.randint(0, 1000)
        return ChangeModel(
            id_old=random.randint(0, 1000),
            ip_old=ip,
            community_old=community,
            sysname_old=sysname,
            ifIndex_old=ifIndex,
            ifName_old="ifName1",
            ifDescr_old="ifDescr1",
            ifAlias_old="ifAlias1",
            ifHighSpeed_old=1000,
            ifOperStatus_old="up",
            ifAdminStatus_old="up",
            id_new=random.randint(0, 1000),
            ip_new=ip,
            community_new=community,
            sysname_new=sysname,
            ifIndex_new=ifIndex,
            ifName_new="ifName2",
            ifDescr_new="ifDescr2",
            ifAlias_new="ifAlias2",
            ifHighSpeed_new=1000,
            ifOperStatus_new="up",
            ifAdminStatus_new="up",
            assigned="unittest"
        )

    def create_table(self) -> None:
        try:
            self.database.open_connection()
            self.database.query_execute(
                f"""CREATE TABLE IF NOT EXISTS {TableNames.CHANGES} (
                    {ChangeField.ID_OLD} SERIAL NOT NULL,
                    {ChangeField.IP_OLD} VARCHAR(15) NOT NULL,
                    {ChangeField.COMMUNITY_OLD} VARCHAR(20) NOT NULL,
                    {ChangeField.SYSNAME_OLD} VARCHAR(20) NOT NULL,
                    {ChangeField.IFINDEX_OLD} INTEGER NOT NULL,
                    {ChangeField.IFNAME_OLD} VARCHAR(20) NOT NULL,
                    {ChangeField.IFDESCR_OLD} VARCHAR(20) NOT NULL,
                    {ChangeField.IFALIAS_OLD} VARCHAR(20) NOT NULL,
                    {ChangeField.IFHIGHSPEED_OLD} INTEGER NOT NULL,
                    {ChangeField.IFOPERSTATUS_OLD} VARCHAR(20) NOT NULL,
                    {ChangeField.IFADMINSTATUS_OLD} VARCHAR(20) NOT NULL,
                    {ChangeField.ID_NEW} SERIAL NOT NULL,
                    {ChangeField.IP_NEW} VARCHAR(15) NOT NULL,
                    {ChangeField.COMMUNITY_NEW} VARCHAR(20) NOT NULL,
                    {ChangeField.SYSNAME_NEW} VARCHAR(20) NOT NULL,
                    {ChangeField.IFINDEX_NEW} INTEGER NOT NULL,
                    {ChangeField.IFNAME_NEW} VARCHAR(20) NOT NULL,
                    {ChangeField.IFDESCR_NEW} VARCHAR(20) NOT NULL,
                    {ChangeField.IFALIAS_NEW} VARCHAR(20) NOT NULL,
                    {ChangeField.IFHIGHSPEED_NEW} INTEGER NOT NULL,
                    {ChangeField.IFOPERSTATUS_NEW} VARCHAR(20) NOT NULL,
                    {ChangeField.IFADMINSTATUS_NEW} VARCHAR(20) NOT NULL,
                    {ChangeField.ASSIGNED} VARCHAR(20) NULL DEFAULT NULL,
                    PRIMARY KEY ({ChangeField.ID_OLD}, {ChangeField.ID_NEW})
                )"""
            )
            self.database.close_connection()
        except Exception as error:
            print(f"Failed unit test. Error change database. {error}")
            exit(1)

    def insert(self, change: ChangeModel) -> None:
        try:
            old_interface = InterfaceModel(
                id=change.id_old,
                ip=change.ip_old,
                community=change.community_old,
                sysname=change.sysname_old,
                ifIndex=change.ifIndex_old,
                ifName=change.ifName_old,
                ifDescr=change.ifDescr_old,
                ifAlias=change.ifAlias_old,
                ifHighSpeed=change.ifHighSpeed_old,
                ifOperStatus=change.ifOperStatus_old,
                ifAdminStatus=change.ifAdminStatus_old,
                consulted_at=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            )
            new_interface = InterfaceModel(
                id=change.id_new,
                ip=change.ip_new,
                community=change.community_new,
                sysname=change.sysname_new,
                ifIndex=change.ifIndex_new,
                ifName=change.ifName_new,
                ifDescr=change.ifDescr_new,
                ifAlias=change.ifAlias_new,
                ifHighSpeed=change.ifHighSpeed_new,
                ifOperStatus=change.ifOperStatus_new,
                ifAdminStatus=change.ifAdminStatus_new,
                consulted_at=datetime.now().strftime("%Y-%m-%d")
            )

            if change.assigned:
                user = UserModel(
                    username=change.assigned,
                    password="test_password",
                    name="unit",
                    lastname="test",
                    status=UserStatusTypes.ACTIVE,
                    role=RoleTypes.ADMIN,
                    created_at=None,
                    updated_at=None
                )
            else: user = None

            self.interface_database.insert(new_interface=old_interface)
            self.interface_database.insert(new_interface=new_interface)
            if user and not self.user_database.get(username=change.assigned): self.user_database.insert(new_user=user)

            old_interface: InterfaceModel = self.interface_database.get(
                ip=old_interface.ip, community=old_interface.community, 
                sysname=old_interface.sysname, ifIndex=old_interface.ifIndex,
                consulted_at=old_interface.consulted_at
            )
            new_interface: InterfaceModel = self.interface_database.get(
                ip=new_interface.ip, community=new_interface.community, 
                sysname=new_interface.sysname, ifIndex=new_interface.ifIndex,
                consulted_at=new_interface.consulted_at
            )

            if not old_interface or not new_interface:
                raise Exception("Failed to insert interfaces")
            
            self.database.open_connection()
            self.database.query_execute(
                f"""
                    INSERT INTO {TableNames.CHANGES} (
                        {ChangeField.ID_OLD},
                        {ChangeField.IP_OLD},
                        {ChangeField.COMMUNITY_OLD},
                        {ChangeField.SYSNAME_OLD},
                        {ChangeField.IFINDEX_OLD},
                        {ChangeField.IFNAME_OLD},
                        {ChangeField.IFDESCR_OLD},
                        {ChangeField.IFALIAS_OLD},
                        {ChangeField.IFHIGHSPEED_OLD},
                        {ChangeField.IFOPERSTATUS_OLD},
                        {ChangeField.IFADMINSTATUS_OLD},
                        {ChangeField.ID_NEW},
                        {ChangeField.IP_NEW},
                        {ChangeField.COMMUNITY_NEW},
                        {ChangeField.SYSNAME_NEW},
                        {ChangeField.IFINDEX_NEW},
                        {ChangeField.IFNAME_NEW},
                        {ChangeField.IFDESCR_NEW},
                        {ChangeField.IFALIAS_NEW},
                        {ChangeField.IFHIGHSPEED_NEW},
                        {ChangeField.IFOPERSTATUS_NEW},
                        {ChangeField.IFADMINSTATUS_NEW},
                        {ChangeField.ASSIGNED}
                    ) VALUES (
                        {old_interface.id},
                        '{old_interface.ip}',
                        '{old_interface.community}',
                        '{old_interface.sysname}',
                        {old_interface.ifIndex},
                        '{old_interface.ifName}',
                        '{old_interface.ifDescr}',
                        '{old_interface.ifAlias}',
                        {old_interface.ifHighSpeed},
                        '{old_interface.ifOperStatus}',
                        '{old_interface.ifAdminStatus}',
                        {new_interface.id},
                        '{new_interface.ip}',
                        '{new_interface.community}',
                        '{new_interface.sysname}',
                        {new_interface.ifIndex},
                        '{new_interface.ifName}',
                        '{new_interface.ifDescr}',
                        '{new_interface.ifAlias}',
                        {new_interface.ifHighSpeed},
                        '{new_interface.ifOperStatus}',
                        '{new_interface.ifAdminStatus}',
                        '{change.assigned}'
                    )
                """
            )
            self.database.close_connection()
        except Exception as error:
            print(f"Failed unit test. Error change database. {error}")
            exit(1)

    def clean(self) -> None:
        try:
            self.database.open_connection()
            self.database.query_execute(f"DELETE FROM {TableNames.CHANGES}")
            self.database.close_connection()
        except Exception as error:
            print(f"Failed unit test. Error change database. {error}")
            exit(1)

class AssignmentDBTest:
    database: DabaseTest
    interface_database: InterfaceDBTest = InterfaceDBTest()
    user_database: UserDBTest = UserDBTest()

    def __init__(self, uri: str | None = None):
        self.database = DabaseTest(uri=uri)

    def get_mock(self) -> AssignmentCompleteModel:
        ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        community = "public" + str(random.randint(0, 1000))
        sysname = "sysname" + str(random.randint(0, 1000))
        ifIndex = random.randint(0, 1000)
        return AssignmentCompleteModel(
            id_old=random.randint(0, 1000),
            ip_old=ip,
            community_old=community,
            sysname_old=sysname,
            ifIndex_old=ifIndex,
            ifName_old="ifName1",
            ifDescr_old="ifDescr1",
            ifAlias_old="ifAlias1",
            ifHighSpeed_old=1000,
            ifOperStatus_old="up",
            ifAdminStatus_old="up",
            id_new=random.randint(0, 1000),
            ip_new=ip,
            community_new=community,
            sysname_new=sysname,
            ifIndex_new=ifIndex,
            ifName_new="ifName2",
            ifDescr_new="ifDescr2",
            ifAlias_new="ifAlias2",
            ifHighSpeed_new=1000,
            ifOperStatus_new="up",
            ifAdminStatus_new="up",
            username="unittest",
            name="Unit",
            lastname="Test",
            assign_by="autounittest",
            type_status=AssignmentStatusTypes.PENDING,
            created_at=datetime.now().strftime("%Y-%m-%d"),
            updated_at=None
        )

    def create_table(self) -> None:
        try:
            self.database.open_connection()
            self.database.query_execute(
                f"""CREATE TABLE IF NOT EXISTS {TableNames.ASSIGNMENTS} (
                    {AssignmentField.OLD_INTERFACE_ID} SERIAL NOT NULL,
                    {AssignmentField.CURRENT_INTERFACE_ID} SERIAL NOT NULL,
                    {AssignmentField.USERNAME} VARCHAR(20) NOT NULL,
                    {AssignmentField.ASSIGN_BY} VARCHAR(20) NOT NULL,
                    {AssignmentField.TYPE_STATUS} VARCHAR(12) NOT NULL,
                    {AssignmentField.CREATED_AT} DATE DEFAULT CURRENT_DATE,
                    {AssignmentField.UPDATED_AT} DATE DEFAULT NULL,
                    CONSTRAINT {TableNames.ASSIGNMENTS}_status CHECK ({AssignmentField.TYPE_STATUS} 
                        IN ('{AssignmentStatusTypes.PENDING}', '{AssignmentStatusTypes.INSPECTED}', '{AssignmentStatusTypes.REDISCOVERED}')),
                    PRIMARY KEY ({AssignmentField.OLD_INTERFACE_ID}, {AssignmentField.USERNAME}, {AssignmentField.ASSIGN_BY})
                )"""
            )
            self.database.close_connection()
        except Exception as error:
            print(f"Failed unit test. Error assignment database. {error}")
            exit(1)

    def insert(self, new_assignment: AssignmentCompleteModel) -> None:
        try:
            old_interface = InterfaceModel(
                id=new_assignment.id_old,
                ip=new_assignment.ip_old,
                community=new_assignment.community_old,
                sysname=new_assignment.sysname_old,
                ifIndex=new_assignment.ifIndex_old,
                ifName=new_assignment.ifName_old,
                ifDescr=new_assignment.ifDescr_old,
                ifAlias=new_assignment.ifAlias_old,
                ifHighSpeed=new_assignment.ifHighSpeed_old,
                ifOperStatus=new_assignment.ifOperStatus_old,
                ifAdminStatus=new_assignment.ifAdminStatus_old,
                consulted_at=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            )
            new_interface = InterfaceModel(
                id=new_assignment.id_new,
                ip=new_assignment.ip_new,
                community=new_assignment.community_new,
                sysname=new_assignment.sysname_new,
                ifIndex=new_assignment.ifIndex_new,
                ifName=new_assignment.ifName_new,
                ifDescr=new_assignment.ifDescr_new,
                ifAlias=new_assignment.ifAlias_new,
                ifHighSpeed=new_assignment.ifHighSpeed_new,
                ifOperStatus=new_assignment.ifOperStatus_new,
                ifAdminStatus=new_assignment.ifAdminStatus_new,
                consulted_at=datetime.now().strftime("%Y-%m-%d")
            )
            user = UserModel(
                username=new_assignment.username,
                password="test_password",
                name=new_assignment.name,
                lastname=new_assignment.lastname,
                status=UserStatusTypes.ACTIVE,
                role=RoleTypes.ADMIN,
                created_at=None,
                updated_at=None
            )

            self.interface_database.insert(new_interface=old_interface)
            self.interface_database.insert(new_interface=new_interface)
            if user and not self.user_database.get(username=new_assignment.username): self.user_database.insert(new_user=user)

            old_interface: InterfaceModel = self.interface_database.get(
                ip=old_interface.ip, community=old_interface.community, 
                sysname=old_interface.sysname, ifIndex=old_interface.ifIndex,
                consulted_at=old_interface.consulted_at
            )
            new_interface: InterfaceModel = self.interface_database.get(
                ip=new_interface.ip, community=new_interface.community, 
                sysname=new_interface.sysname, ifIndex=new_interface.ifIndex,
                consulted_at=new_interface.consulted_at
            )

            if not old_interface or not new_interface:
                raise Exception("Failed to insert interfaces")
            
            self.database.open_connection()
            self.database.query_execute(
                f"""
                    INSERT INTO {TableNames.ASSIGNMENTS} (
                        {AssignmentField.OLD_INTERFACE_ID},
                        {AssignmentField.CURRENT_INTERFACE_ID},
                        {AssignmentField.USERNAME},
                        {AssignmentField.ASSIGN_BY},
                        {AssignmentField.TYPE_STATUS}
                    ) VALUES (
                        {old_interface.id},
                        {new_interface.id},
                        '{new_assignment.username}',
                        '{new_assignment.assign_by}',
                        '{new_assignment.type_status}'
                    )
                """
            )
            self.database.close_connection()
        except Exception as error:
            print(f"Failed unit test. Error assingment database. {error}")
            exit(1)

    def clean(self) -> None:
        try:
            self.database.open_connection()
            self.database.query_execute(f"DELETE FROM {TableNames.ASSIGNMENTS}")
            self.database.close_connection()
        except Exception as error:
            print(f"Failed unit test. Error assignment database. {error}")
            exit(1)


if __name__ == "__main__":
    database = DabaseTest()
    database.open_connection()
    database.query_execute(
        """CREATE TABLE IF NOT EXISTS test (
            id SERIAL PRIMARY KEY, 
            name VARCHAR(20) NOT NULL
        )"""
    )
    database.query_execute("INSERT INTO test (name) VALUES ('test')")
    database.query_execute("DELETE FROM test")
    database.query_execute("DROP TABLE IF EXISTS test")
    database.close_connection()
