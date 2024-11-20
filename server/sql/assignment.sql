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