CREATE TABLE operator (
    username VARCHAR(20) PRIMARY KEY,
    name VARCHAR(30) NOT NULL, 
    lastname VARCHAR(30) NOT NULL,
    password VARCHAR(64) NOT NULL,
	profile VARCHAR(10) NOT NULL,
	statusAccount VARCHAR(8) NOT NULL,
    createdAt DATE DEFAULT NOW(),
    CONSTRAINT type_profile CHECK (profile IN ('SUPERADMIN', 'ADMIN', 'STANDARD', 'SOPORT')),
    CONSTRAINT status_account CHECK (statusAccount IN ('ACTIVE', 'INACTIVE', 'DELETED'))
);