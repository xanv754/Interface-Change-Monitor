from data.constants.database import TableNames
from constants.fields import InterfaceField, ChangeField


CHANGE_SCHEMA = f"""
    CREATE TABLE IF NOT EXISTS {TableNames.CHANGES} (
        {ChangeField.ID_OLD} SERIAL NOT NULL,
        {ChangeField.IP_OLD} VARCHAR(15) NOT NULL,
        {ChangeField.COMMUNITY_OLD} VARCHAR(20) NOT NULL,
        {ChangeField.SYSNAME_OLD} VARCHAR(20) NOT NULL,
        {ChangeField.IFINDEX_OLD} NUMERIC NOT NULL,
        {ChangeField.IFNAME_OLD} VARCHAR NOT NULL,
        {ChangeField.IFDESCR_OLD} VARCHAR NOT NULL,
        {ChangeField.IFALIAS_OLD} VARCHAR NOT NULL,
        {ChangeField.IFHIGHSPEED_OLD} NUMERIC NOT NULL,
        {ChangeField.IFOPERSTATUS_OLD} VARCHAR(20) NOT NULL,
        {ChangeField.IFADMINSTATUS_OLD} VARCHAR(20) NOT NULL,
        {ChangeField.ID_NEW} SERIAL NOT NULL,
        {ChangeField.IP_NEW} VARCHAR(15) NOT NULL,
        {ChangeField.COMMUNITY_NEW} VARCHAR(20) NOT NULL,
        {ChangeField.SYSNAME_NEW} VARCHAR(20) NOT NULL,
        {ChangeField.IFINDEX_NEW} NUMERIC NOT NULL,
        {ChangeField.IFNAME_NEW} VARCHAR NOT NULL,
        {ChangeField.IFDESCR_NEW} VARCHAR NOT NULL,
        {ChangeField.IFALIAS_NEW} VARCHAR NOT NULL,
        {ChangeField.IFHIGHSPEED_NEW} NUMERIC NOT NULL,
        {ChangeField.IFOPERSTATUS_NEW} VARCHAR(20) NOT NULL,
        {ChangeField.IFADMINSTATUS_NEW} VARCHAR(20) NOT NULL,
        {ChangeField.ASSIGNED} VARCHAR(20) NULL DEFAULT NULL,
        CONSTRAINT {TableNames.CHANGES}_current_interface_id FOREIGN KEY ({ChangeField.ID_NEW}) 
            REFERENCES {TableNames.INTERFACES}({InterfaceField.ID}),
        CONSTRAINT {TableNames.CHANGES}_old_interface_id FOREIGN KEY ({ChangeField.ID_OLD}) 
            REFERENCES {TableNames.INTERFACES}({InterfaceField.ID}),
        PRIMARY KEY ({ChangeField.ID_OLD}, {ChangeField.ID_NEW})
    )
"""