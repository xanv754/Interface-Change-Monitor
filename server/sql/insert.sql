INSERT INTO equipment (ip, community, sysname)
VALUES
  ('192.168.1.1', 'public', 'Router1');

INSERT INTO interface (ifIndex, 
                      idEquipment, 
                      dateConsult, 
                      dateType,
                      ifName, 
                      ifDescr, 
                      ifAlias, 
                      ifSpeed, 
                      ifHighSpeed, 
                      ifPhysAddress, 
                      ifType, 
                      ifOperStatus, 
                      ifAdminStatus, 
                      ifPromiscuousMode, 
                      ifConnectorPresent, 
                      ifLastCheck)
VALUES
  (182, 1, '2023-11-18', 'YESTERDAY', 'GigabitEthernet0/1', 'Interface 1', 'GE0/1', 100, 1000, '00:00:00:00:00:00', 'ethernetCsmacd', 'DOWN', 'UP', FALSE, FALSE, '0:00:00.00'),
  (100, 1, '2023-11-19', 'TODAY', 'GigabitEthernet0/1', 'Interface 1', 'GE0/1', 100, 1000, '00:00:00:00:00:00', 'ethernetCsmacd', 'UP', 'UP', FALSE, FALSE, '0:00:00.00');

INSERT INTO operator (username, name, lastname, password, profile, statusAccount)
VALUES
  ('user', 'Pepe', 'Perez', 'secret123', 'STANDARD', 'ACTIVE'),
  ('user1', 'Manuel', 'Peterson', 'secret123', 'STANDARD', 'ACTIVE'),
  ('user2', 'Gerardo', 'Gonzalez', 'secret123', 'ADMIN', 'ACTIVE'),
  ('user3', 'Patricio', 'Estrella', 'fondoDeBikini', 'SUPERADMIN', 'DELETED'),
  ('user4', 'Wilman', 'Eugenio', 'disleixaAProposito', 'SUPERADMIN', 'INACTIVE'),
  ('USER5', 'Angyee', 'Marin', '123', 'SUPERADMIN', 'ACTIVE');

INSERT INTO assignment (changeInterface, oldInterface, operator, dateAssignment, statusAssignment, assignedBy)
VALUES
  (2, 1, 'user1', '2024-11-20', 'PENDING', 'Angyee Marin');