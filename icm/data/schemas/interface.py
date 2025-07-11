from icm.constants import InterfaceField
from icm.data.constants.database import TableNames


INTERFACE_SCHEMA = f"""
    CREATE TABLE IF NOT EXISTS {TableNames.INTERFACES} (
        {InterfaceField.ID} SERIAL PRIMARY KEY,
        {InterfaceField.IP} VARCHAR(15) NOT NULL,
        {InterfaceField.COMMUNITY} VARCHAR(100) NOT NULL,
        {InterfaceField.SYSNAME} VARCHAR(100) NOT NULL,
        {InterfaceField.IFINDEX} NUMERIC NOT NULL,
        {InterfaceField.IFNAME} VARCHAR NULL,
        {InterfaceField.IFDESCR} VARCHAR NULL,
        {InterfaceField.IFALIAS} VARCHAR NULL,
        {InterfaceField.IFHIGHSPEED} NUMERIC NULL,
        {InterfaceField.IFOPERSTATUS} VARCHAR(100) NULL,
        {InterfaceField.IFADMINSTATUS} VARCHAR(100) NULL,
        {InterfaceField.CONSULTED_AT} DATE NOT NULL,
        CONSTRAINT {TableNames.INTERFACES}_unique UNIQUE (
            {InterfaceField.IP}, 
            {InterfaceField.COMMUNITY},
            {InterfaceField.SYSNAME},
            {InterfaceField.IFINDEX},
            {InterfaceField.CONSULTED_AT}
        )
    )
"""
