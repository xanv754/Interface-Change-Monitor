INSERT INTO equipment (ip, community, sysname)
VALUES
  ('192.168.1.1', 'public', 'Router1');

INSERT INTO interface (ifIndex, idEquipment, dateConsult, dateType,ifName, ifDescr, ifAlias, ifSpeed, ifHighSpeed, ifPhysAddress, ifType, ifOperStatus, ifAdminStatus, ifPromiscuousMode, ifConnectorPresent, ifLastCheck)
VALUES
  (100, 'GigabitEthernet0/1', 'Interface 1', 'GE0/1', 100, 1000, '00:00:00:00:00:00', 'ethernetCsmacd', 'UP', 'UP', FALSE, FALSE, '2023-11-11');

INSERT INTO operator (username, name, lastname, password, profile, statusAccount, deleteOperator)
VALUES
  ('user1', 'Manuel', 'Peterson', 'secret123', 'STANDARD', 'ACTIVE');