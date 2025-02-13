from constants import InterfaceType, StatusType
from database import GTABLES, InterfaceSchema, EquipmentSchema

TABLE_SCHEMA_INTERFACE = f"""
    CREATE TABLE {GTABLES.INTERFACE.value} (
        {InterfaceSchema.ID.value} SERIAL PRIMARY KEY, 
        {InterfaceSchema.IFINDEX.value} INTEGER NOT NULL,
        {InterfaceSchema.ID_EQUIPMENT.value} SERIAL REFERENCES {GTABLES.EQUIPMENT.value}({EquipmentSchema.ID.value}) ON DELETE CASCADE,
        {InterfaceSchema.DATE_CONSULT.value} DATE NOT NULL,
        {InterfaceSchema.INTERFACE_TYPE.value} VARCHAR(3) NOT NULL,
        {InterfaceSchema.IFNAME.value} VARCHAR(200) NOT NULL,
        {InterfaceSchema.IFDESCR.value} VARCHAR(200) NOT NULL,
        {InterfaceSchema.IFALIAS.value} VARCHAR(200) NOT NULL,
        {InterfaceSchema.IFSPEED.value} NUMERIC(11) NOT NULL,
        {InterfaceSchema.IFHIGHSPEED.value} NUMERIC(11) NOT NULL,
        {InterfaceSchema.IFPHYSADDRESS.value} VARCHAR(18) NOT NULL,
        {InterfaceSchema.IFTYPE.value} VARCHAR(200) NOT NULL,
        {InterfaceSchema.IFOPERSTATUS.value} VARCHAR(15) NOT NULL,
        {InterfaceSchema.IFADMINSTATUS.value} VARCHAR(15) NOT NULL,
        {InterfaceSchema.IFPROMISCUOUSMODE.value} BOOLEAN NOT NULL,
        {InterfaceSchema.IFCONNECTORPRESENT.value} BOOLEAN NOT NULL,
        {InterfaceSchema.IFLASTCHECK.value} VARCHAR(40) NOT NULL,
        CONSTRAINT new_interface UNIQUE (
            {InterfaceSchema.ID_EQUIPMENT.value}, 
            {InterfaceSchema.IFINDEX.value}, 
            {InterfaceSchema.INTERFACE_TYPE.value}
        ),
        CONSTRAINT type_status_operator CHECK (
            {InterfaceSchema.IFOPERSTATUS.value} IN (
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
            {InterfaceSchema.IFADMINSTATUS.value} IN (
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
            {InterfaceSchema.INTERFACE_TYPE.value} IN (
                '{InterfaceType.NEW.value}', 
                '{InterfaceType.OLD.value}'
            )
        )
    );                
"""