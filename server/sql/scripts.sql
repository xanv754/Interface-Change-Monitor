CREATE TABLE equipment (
    ip VARCHAR(15) UNIQUE NOT NULL,
    community VARCHAR(30) UNIQUE NOT NULL,
    sysname VARCHAR(30) NOT NULL,
    createdAt TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updatedAt TIMESTAMP DEFAULT NULL,
	PRIMARY KEY (ip, community)
);

INSERT INTO equipment (ip, community, sysname)
VALUES
  ('192.168.1.1', 'public', 'Router1');

SELECT * FROM equipment;

DELETE FROM equipment;

DROP TABLE equipment;

CREATE TABLE interface (
  id SERIAL PRIMARY KEY, 
  ifIndex INTEGER NOT NULL,
  ip VARCHAR(15) REFERENCES equipment(ip) ON DELETE CASCADE,
  community VARCHAR(30) REFERENCES equipment(community) ON DELETE CASCADE,
  dateConsult DATE NOT NULL,
  dateType VARCHAR(10) NOT NULL,
  ifName VARCHAR(200) NOT NULL,
  ifDescr VARCHAR(200) NOT NULL,
  ifAlias VARCHAR(200) NOT NULL,
  ifSpeed NUMERIC(11) NOT NULL,
  ifHighSpeed NUMERIC(11) NOT NULL,
  ifPhysAddress VARCHAR(18) NOT NULL,
  ifType VARCHAR(200) NOT NULL,
  ifOperStatus VARCHAR(15) NOT NULL,
  ifAdminStatus VARCHAR(15) NOT NULL,
  ifPromiscuousMode BOOLEAN NOT NULL,
  ifConnectorPresent BOOLEAN NOT NULL,
  ifLastCheck VARCHAR(40) NOT NULL,
  CONSTRAINT type_date CHECK (dateType IN ('TODAY', 'YESTERDAY', 'OLD')),
  CONSTRAINT type_status_operator CHECK (ifOperStatus IN ('UP', 'DOWN', 'TESTING', 'DORMANT', 'UNKNOWN', 'NOTPRESENT', 'LOWERLAYERDOWN', 'DEFAULT')),
  CONSTRAINT type_status_administration CHECK (ifAdminStatus IN ('UP', 'DOWN', 'TESTING', 'DORMANT', 'UNKNOWN', 'NOTPRESENT', 'LOWERLAYERDOWN', 'DEFAULT'))
);

INSERT INTO interface (ifIndex, ip, community, dateConsult, dateType,ifName, ifDescr, ifAlias, ifSpeed, ifHighSpeed, ifPhysAddress, ifType, ifOperStatus, ifAdminStatus, ifPromiscuousMode, ifConnectorPresent, ifLastCheck)
VALUES
  (100, '192.168.1.1', 'public', '2023-11-18', 'YESTERDAY', 'GigabitEthernet0/1', 'Interface 1', 'GE0/1', 100, 1000, '00:00:00:00:00:00', 'ethernetCsmacd', 'DOWN', 'UP', FALSE, FALSE, '0:00:00.00'),
  (100, '192.168.1.1', 'public', '2023-11-19', 'TODAY', 'GigabitEthernet0/1', 'Interface 1', 'GE0/1', 100, 1000, '00:00:00:00:00:00', 'ethernetCsmacd', 'UP', 'UP', FALSE, FALSE, '0:00:00.00');

SELECT * FROM interface;

DELETE FROM interface;

DROP TABLE interface;

CREATE TABLE operator (
    username VARCHAR(20) PRIMARY KEY,
    name VARCHAR(30) NOT NULL, 
    lastname VARCHAR(30) NOT NULL,
    password VARCHAR(64) NOT NULL,
	profile VARCHAR(10) NOT NULL,
	statusAccount VARCHAR(8) NOT NULL,
    deleteOperator BOOLEAN NOT NULL,
    CONSTRAINT type_profile CHECK (profile IN ('SUPERADMIN', 'ADMIN', 'STANDARD', 'SOPORT')),
    CONSTRAINT status_account CHECK (statusAccount IN ('ACTIVE', 'INACTIVE'))
);

INSERT INTO operator (username, name, lastname, password, profile, statusAccount, deleteOperator)
VALUES
  ('user1', 'Manuel', 'Peterson', 'secret123', 'STANDARD', 'ACTIVE', FALSE),
  ('user2', 'Gerardo', 'Gonzalez', 'secret123', 'ADMIN', 'ACTIVE', FALSE),
  ('user3', 'Patricio', 'Estrella', 'fondoDeBikini', 'SUPERADMIN', 'ACTIVE', FALSE),
  ('user4', 'Wilman', 'Eugenio', 'disleixaAProposito', 'SUPERADMIN', 'INACTIVE', FALSE);

SELECT * FROM operator;

DELETE FROM operator;

DROP TABLE operator;

CREATE TABLE assignment (
  idInterfaceToday SERIAL REFERENCES interface(id) ON DELETE CASCADE,
  idInterfaceYesterday SERIAL REFERENCES interface(id) ON DELETE CASCADE,
  operator VARCHAR(20) REFERENCES operator(username) ON DELETE CASCADE,
  dateAssignment DATE NOT NULL,
  statusAssignment VARCHAR(100) NOT NULL,
  assignedBy VARCHAR(60) NOT NULL,
  dateReview DATE DEFAULT NULL,
  PRIMARY KEY (idInterfaceToday, idInterfaceYesterday, operator),
  CONSTRAINT type_status_assignment CHECK (statusAssignment IN ('PENDING', 'REVIEW', 'REDISCOVER'))
);

INSERT INTO assignment (idInterfaceToday, idInterfaceYesterday, operator, dateAssignment, statusAssignment, assignedBy)
VALUES
  (2, 1, 'user1', '2024-11-20', 'PENDING', 'Angyee Marin');
  
SELECT * FROM assignment;

DELETE FROM assignment;

DROP TABLE assignment;