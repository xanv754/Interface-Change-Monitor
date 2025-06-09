from constants.types import AssignmentStatusTypes
from database.constants.database import TableNames
from models.interface import InterfaceField
from models.user import UserField
from models.assignment import AssignmentField


ASSIGNMENT_SCHEMA = f"""
    CREATE TABLE IF NOT EXISTS {TableNames.ASSIGNMENTS} (
        {AssignmentField.OLD_INTERFACE_ID} SERIAL NOT NULL,
        {AssignmentField.CURRENT_INTERFACE_ID} SERIAL NOT NULL,
        {AssignmentField.USERNAME} VARCHAR(20) NOT NULL,
        {AssignmentField.ASSIGN_BY} VARCHAR(20) NOT NULL,
        {AssignmentField.TYPE_STATUS} VARCHAR(12) NOT NULL,
        {AssignmentField.CREATED_AT} DATE DEFAULT CURRENT_DATE,
        {AssignmentField.UPDATED_AT} DATE DEFAULT NULL,
        CONSTRAINT {TableNames.ASSIGNMENTS}_status CHECK ({AssignmentField.TYPE_STATUS} 
            IN ('{AssignmentStatusTypes.PENDING}', '{AssignmentStatusTypes.INSPECTED}', '{AssignmentStatusTypes.REDISCOVERED}')),
        CONSTRAINT {TableNames.ASSIGNMENTS}_user_id FOREIGN KEY ({AssignmentField.USERNAME}) 
            REFERENCES {TableNames.USERS}({UserField.USERNAME}),
        CONSTRAINT {TableNames.ASSIGNMENTS}_old_interface_id FOREIGN KEY ({AssignmentField.OLD_INTERFACE_ID}) 
            REFERENCES {TableNames.INTERFACES}({InterfaceField.ID}),
        constraint {TableNames.ASSIGNMENTS}_current_interface_id FOREIGN KEY ({AssignmentField.CURRENT_INTERFACE_ID}) 
            REFERENCES {TableNames.INTERFACES}({InterfaceField.ID}),
        PRIMARY KEY ({AssignmentField.OLD_INTERFACE_ID}, {AssignmentField.USERNAME}, {AssignmentField.ASSIGN_BY})
    )
"""