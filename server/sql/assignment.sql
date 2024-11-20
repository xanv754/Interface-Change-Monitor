CREATE TABLE assignment (
  idInterfaceToday INTEGER REFERENCES interface(ifIndex) ON DELETE CASCADE,
  idEquipmentToday VARCHAR REFERENCES Interface(idEquipment) ON DELETE CASCADE,
  idInterfaceYesterday INTEGER REFERENCES interface(ifIndex) ON DELETE CASCADE,
  idEquipmentYesterday VARCHAR REFERENCES Interface(idEquipment) ON DELETE CASCADE,
  idOperator VARCHAR(20) REFERENCES operator(username) ON DELETE CASCADE,
  dateAssignment DATE NOT NULL,
  statusAssignment VARCHAR(100) NOT NULL,
  assignedBy VARCHAR(60) NOT NULL,
  dateReview DATE DEFAULT NULL,
  PRIMARY KEY (idInterfaceToday, idEquipmentToday, idInterfaceYesterday, idEquipmentYesterday, idOperator),
  CONSTRAINT type_status_assignment CHECK (statusAssignment IN ('PENDING', 'REVIEW', 'REDISCOVER')),
);
