from database.constants.database import TableNames
from models.interface import InterfaceField
from models.user import UserField
from models.change import ChangeField


CHANGE_SCHEMA = f"""
    CREATE TABLE IF NOT EXISTS {TableNames.CHANGES} (
        {ChangeField.CURRENT_INTERFACE_ID} INTEGER NOT NULL,
        {ChangeField.OLD_INTERFACE_ID} INTEGER NOT NULL,
        {ChangeField.ASSIGNED} VARCHAR(20) NULL DEFAULT NULL,
        CONSTRAINT {TableNames.CHANGES}_current_interface_id FOREIGN KEY ({ChangeField.CURRENT_INTERFACE_ID}) 
            REFERENCES {TableNames.INTERFACES}({InterfaceField.ID}),
        CONSTRAINT {TableNames.CHANGES}_old_interface_id FOREIGN KEY ({ChangeField.OLD_INTERFACE_ID}) 
            REFERENCES {TableNames.INTERFACES}({InterfaceField.ID}),
        PRIMARY KEY ({ChangeField.CURRENT_INTERFACE_ID}, {ChangeField.OLD_INTERFACE_ID})
    )
"""