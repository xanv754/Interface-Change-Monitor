from database import GTABLES, EquipmentSchema

TABLE_SCHEMA_EQUIPMENT = f"""
    CREATE TABLE {GTABLES.EQUIPMENT.value} (
        {EquipmentSchema.ID.value} SERIAL PRIMARY KEY,
        {EquipmentSchema.IP.value} VARCHAR(15) UNIQUE NOT NULL,
        {EquipmentSchema.COMMUNITY.value} VARCHAR(30) UNIQUE NOT NULL,
        {EquipmentSchema.SYSNAME.value} VARCHAR(30) NULL,
        {EquipmentSchema.CREATED_AT.value} DATE DEFAULT NOW(),
        {EquipmentSchema.UPDATED_AT.value} DATE DEFAULT NULL,
        CONSTRAINT new_equipment UNIQUE (
            {EquipmentSchema.IP.value}, 
            {EquipmentSchema.COMMUNITY.value}
        )
    );
"""