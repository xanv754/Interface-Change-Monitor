from icm.constants import RoleTypes, UserStatusTypes, UserField
from icm.data.constants.database import TableNames


USER_SCHEMA = f"""
    CREATE TABLE IF NOT EXISTS {TableNames.USERS} (
        {UserField.USERNAME} VARCHAR(20) PRIMARY KEY,
        {UserField.PASSWORD} VARCHAR(100) NOT NULL,
        {UserField.NAME} VARCHAR(50) NOT NULL,
        {UserField.LASTNAME} VARCHAR(50) NOT NULL,
        {UserField.STATUS} VARCHAR(8) NOT NULL,
        {UserField.ROLE} VARCHAR(6) NOT NULL,
        {UserField.CREATED_AT} DATE DEFAULT CURRENT_DATE,
        {UserField.UPDATED_AT} DATE DEFAULT NULL,
        CONSTRAINT {TableNames.USERS}_status CHECK ({UserField.STATUS} IN ('{UserStatusTypes.ACTIVE}', '{UserStatusTypes.INACTIVE}', '{UserStatusTypes.DELETED}')),
        CONSTRAINT {TableNames.USERS}_role CHECK ({UserField.ROLE} IN ('{RoleTypes.ADMIN}', '{RoleTypes.ROOT}', '{RoleTypes.USER}', '{RoleTypes.SOPORT}'))
    )
"""
