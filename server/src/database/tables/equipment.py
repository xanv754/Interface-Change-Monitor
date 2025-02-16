"""SQL script to create the equipment table."""

from database import GTABLES, EquipmentSchemaDB

TABLE_SCHEMA_EQUIPMENT = f"""
    CREATE TABLE {GTABLES.EQUIPMENT.value} (
        {EquipmentSchemaDB.ID.value} SERIAL PRIMARY KEY,
        {EquipmentSchemaDB.IP.value} VARCHAR(15) UNIQUE NOT NULL,
        {EquipmentSchemaDB.COMMUNITY.value} VARCHAR(30) UNIQUE NOT NULL,
        {EquipmentSchemaDB.SYSNAME.value} VARCHAR(30) NULL,
        {EquipmentSchemaDB.CREATED_AT.value} DATE DEFAULT NOW(),
        {EquipmentSchemaDB.UPDATED_AT.value} DATE DEFAULT NULL,
        CONSTRAINT new_equipment UNIQUE (
            {EquipmentSchemaDB.IP.value}, 
            {EquipmentSchemaDB.COMMUNITY.value}
        )
    );
"""
