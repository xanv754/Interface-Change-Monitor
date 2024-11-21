CREATE TABLE equipment (
    id SERIAL PRIMARY KEY,
    ip VARCHAR(15) UNIQUE NOT NULL,
    community VARCHAR(30) UNIQUE NOT NULL,
    sysname VARCHAR(30) NOT NULL,
    createdAt TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updatedAt TIMESTAMP DEFAULT NULL,
    CONSTRAINT new_equipment UNIQUE (ip, community)
);
