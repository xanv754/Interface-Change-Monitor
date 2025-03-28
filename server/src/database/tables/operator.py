"""SQL script to create the operator table."""

from constants import ProfileType, AccountType
from database import GTABLES, OperatorSchemaDB

TABLE_SCHEMA_OPERATOR = f"""
    CREATE TABLE {GTABLES.OPERATOR.value} (
        {OperatorSchemaDB.USERNAME.value} VARCHAR(20) PRIMARY KEY,
        {OperatorSchemaDB.NAME.value} VARCHAR(30) NOT NULL,
        {OperatorSchemaDB.LASTNAME.value} VARCHAR(30) NOT NULL,
        {OperatorSchemaDB.PASSWORD.value} VARCHAR(64) NOT NULL,
        {OperatorSchemaDB.PROFILE.value} VARCHAR(10) NOT NULL,
        {OperatorSchemaDB.STATUS_ACCOUNT.value} VARCHAR(8) NOT NULL,
        {OperatorSchemaDB.CREATED_AT.value} DATE DEFAULT NOW(),
        CONSTRAINT type_profile CHECK (
            {OperatorSchemaDB.PROFILE.value} IN (
                '{ProfileType.ROOT.value}',
                '{ProfileType.ADMIN.value}',
                '{ProfileType.STANDARD.value}',
                '{ProfileType.SOPORT.value}'
            )
        ),
        CONSTRAINT status_account CHECK (
            {OperatorSchemaDB.STATUS_ACCOUNT.value} IN (
                '{AccountType.ACTIVE.value}',
                '{AccountType.INACTIVE.value}',
                '{AccountType.DELETED.value}'
            )
        )
    );
"""
