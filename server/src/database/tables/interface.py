"""SQL script to create the interface table."""
from constants.types import InterfaceType, StatusType
from database.constants.tables import Tables as GTABLES # Global Tables
from database.schemas.interface import InterfaceSchemaDB
from database.schemas.equipment import EquipmentSchemaDB


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
        {InterfaceSchemaDB.IFHIGHSPEED.value} NUMERIC(11) NOT NULL,
        {InterfaceSchemaDB.IFOPERSTATUS.value} VARCHAR(15) NOT NULL,
        {InterfaceSchemaDB.IFADMINSTATUS.value} VARCHAR(15) NOT NULL,
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
