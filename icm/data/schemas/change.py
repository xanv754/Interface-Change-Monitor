from icm.constants import InterfaceField, ChangeField
from icm.data.constants.database import TableNames


CHANGE_SCHEMA = f"""
    CREATE TABLE IF NOT EXISTS {TableNames.CHANGES} (
        {ChangeField.ID_OLD} SERIAL NOT NULL,
        {ChangeField.IP_OLD} VARCHAR(15) NOT NULL,
        {ChangeField.COMMUNITY_OLD} VARCHAR NOT NULL,
        {ChangeField.SYSNAME_OLD} VARCHAR NOT NULL,
        {ChangeField.IFINDEX_OLD} VARCHAR NOT NULL,
        {ChangeField.IFNAME_OLD} VARCHAR NULL,
        {ChangeField.IFDESCR_OLD} VARCHAR NULL,
        {ChangeField.IFALIAS_OLD} VARCHAR NULL,
        {ChangeField.IFHIGHSPEED_OLD} VARCHAR NULL,
        {ChangeField.IFOPERSTATUS_OLD} VARCHAR(20) NULL,
        {ChangeField.IFADMINSTATUS_OLD} VARCHAR(20) NULL,
        {ChangeField.ID_NEW} SERIAL NOT NULL,
        {ChangeField.IP_NEW} VARCHAR(15) NOT NULL,
        {ChangeField.COMMUNITY_NEW} VARCHAR NOT NULL,
        {ChangeField.SYSNAME_NEW} VARCHAR NOT NULL,
        {ChangeField.IFINDEX_NEW} VARCHAR NOT NULL,
        {ChangeField.IFNAME_NEW} VARCHAR NULL,
        {ChangeField.IFDESCR_NEW} VARCHAR NULL,
        {ChangeField.IFALIAS_NEW} VARCHAR NULL,
        {ChangeField.IFHIGHSPEED_NEW} VARCHAR NULL,
        {ChangeField.IFOPERSTATUS_NEW} VARCHAR(100) NULL,
        {ChangeField.IFADMINSTATUS_NEW} VARCHAR(100) NULL,
        {ChangeField.ASSIGNED} VARCHAR(100) NULL DEFAULT NULL,
        CONSTRAINT {TableNames.CHANGES}_current_interface_id FOREIGN KEY ({ChangeField.ID_NEW}) 
            REFERENCES {TableNames.INTERFACES}({InterfaceField.ID}),
        CONSTRAINT {TableNames.CHANGES}_old_interface_id FOREIGN KEY ({ChangeField.ID_OLD}) 
            REFERENCES {TableNames.INTERFACES}({InterfaceField.ID}),
        PRIMARY KEY ({ChangeField.ID_OLD}, {ChangeField.ID_NEW})
    )
"""
