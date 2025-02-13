from constants import ProfileType, AccountType
from database import GTABLES, OperatorSchema

TABLE_SCHEMA_OPERATOR = f"""
    CREATE TABLE {GTABLES.OPERATOR.value} (
        {OperatorSchema.USERNAME.value} VARCHAR(20) PRIMARY KEY,
        {OperatorSchema.NAME.value} VARCHAR(30) NOT NULL, 
        {OperatorSchema.LASTNAME.value} VARCHAR(30) NOT NULL,
        {OperatorSchema.PASSWORD.value} VARCHAR(64) NOT NULL,
        {OperatorSchema.PROFILE.value} VARCHAR(10) NOT NULL,
        {OperatorSchema.STATUS_ACCOUNT.value} VARCHAR(8) NOT NULL,
        {OperatorSchema.CREATED_AT.value} DATE DEFAULT NOW(),
        CONSTRAINT type_profile CHECK (
            {OperatorSchema.PROFILE.value} IN (
                '{ProfileType.ROOT.value}', 
                '{ProfileType.ADMIN.value}', 
                '{ProfileType.STANDARD.value}', 
                '{ProfileType.SOPORT.value}'
            )
        ),
        CONSTRAINT status_account CHECK (
            {OperatorSchema.STATUS_ACCOUNT.value} IN (
                '{AccountType.ACTIVE.value}', 
                '{AccountType.INACTIVE.value}', 
                '{AccountType.DELETED.value}'
            )
        )
    );   
"""