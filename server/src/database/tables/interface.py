"""SQL script to create the interface table."""

from constants import InterfaceType, StatusType
from database import GTABLES, InterfaceSchemaDB, EquipmentSchemaDB

TABLE_SCHEMA_INTERFACE = f"""
    CREATE TABLE {GTABLES.INTERFACE.value} (
        {InterfaceSchemaDB.ID.value} SERIAL PRIMARY KEY, 
        {InterfaceSchemaDB.IFINDEX.value} INTEGER NOT NULL,
        {InterfaceSchemaDB.ID_EQUIPMENT.value} SERIAL REFERENCES {GTABLES.EQUIPMENT.value}({EquipmentSchemaDB.ID.value}) ON DELETE CASCADE,
        {InterfaceSchemaDB.DATE_CONSULT.value} DATE NOT NULL,
        {InterfaceSchemaDB.INTERFACE_TYPE.value} VARCHAR(3) NOT NULL,
        {InterfaceSchemaDB.IFNAME.value} VARCHAR(200) NOT NULL,
        {InterfaceSchemaDB.IFDESCR.value} VARCHAR(200) NOT NULL,
        {InterfaceSchemaDB.IFALIAS.value} VARCHAR(200) NOT NULL,
        {InterfaceSchemaDB.IFSPEED.value} NUMERIC(11) NOT NULL,
        {InterfaceSchemaDB.IFHIGHSPEED.value} NUMERIC(11) NOT NULL,
        {InterfaceSchemaDB.IFPHYSADDRESS.value} VARCHAR(18) NOT NULL,
        {InterfaceSchemaDB.IFTYPE.value} VARCHAR(200) NOT NULL,
        {InterfaceSchemaDB.IFOPERSTATUS.value} VARCHAR(15) NOT NULL,
        {InterfaceSchemaDB.IFADMINSTATUS.value} VARCHAR(15) NOT NULL,
        {InterfaceSchemaDB.IFPROMISCUOUSMODE.value} BOOLEAN NOT NULL,
        {InterfaceSchemaDB.IFCONNECTORPRESENT.value} BOOLEAN NOT NULL,
        {InterfaceSchemaDB.IFLASTCHECK.value} VARCHAR(40) NOT NULL,
        CONSTRAINT new_interface UNIQUE (
            {InterfaceSchemaDB.ID_EQUIPMENT.value}, 
            {InterfaceSchemaDB.IFINDEX.value}, 
            {InterfaceSchemaDB.INTERFACE_TYPE.value}
        ),
        CONSTRAINT type_status_operator CHECK (
            {InterfaceSchemaDB.IFOPERSTATUS.value} IN (
                '{StatusType.UP.value}', 
                '{StatusType.DOWN.value}', 
                '{StatusType.TESTING.value}', 
                '{StatusType.DORMANT.value}', 
                '{StatusType.UNKNOWN.value}', 
                '{StatusType.NOTPRESENT.value}', 
                '{StatusType.LOWERLAYERDOWN.value}', 
                '{StatusType.DEFAULT.value}'
            )
        ),
        CONSTRAINT type_status_administration CHECK (
            {InterfaceSchemaDB.IFADMINSTATUS.value} IN (
                '{StatusType.UP.value}', 
                '{StatusType.DOWN.value}', 
                '{StatusType.TESTING.value}', 
                '{StatusType.DORMANT.value}', 
                '{StatusType.UNKNOWN.value}', 
                '{StatusType.NOTPRESENT.value}', 
                '{StatusType.LOWERLAYERDOWN.value}', 
                '{StatusType.DEFAULT.value}'
            )
        ),
        CONSTRAINT type_interface CHECK (
            {InterfaceSchemaDB.INTERFACE_TYPE.value} IN (
                '{InterfaceType.NEW.value}', 
                '{InterfaceType.OLD.value}'
            )
        )
    );                
"""
