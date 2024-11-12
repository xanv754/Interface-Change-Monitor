CREATE TABLE equipment (
    id SERIAL PRIMARY KEY,
    ip VARCHAR(15) NOT NULL,
    community VARCHAR(30) NOT NULL,
    sysname VARCHAR(30) NOT NULL
);

INSERT INTO equipment (ip, community, sysname)
VALUES
  ('192.168.1.1', 'public', 'Router1'),
  ('10.0.0.1', 'private', 'Switch2'),
  ('172.16.0.1', 'cisco', 'Firewall3');