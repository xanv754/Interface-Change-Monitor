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