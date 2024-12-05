CREATE TABLE assignment (
  id SERIAL PRIMARY KEY,
  changeInterface SERIAL REFERENCES interface(id) ON DELETE CASCADE,
  oldInterface SERIAL REFERENCES interface(id) ON DELETE CASCADE,
  operator VARCHAR(20) REFERENCES operator(username) ON DELETE CASCADE,
  dateAssignment DATE NOT NULL,
  statusAssignment VARCHAR(100) NOT NULL,
  assignedBy VARCHAR(60) NOT NULL,
  updatedAt DATE DEFAULT NULL,
  CONSTRAINT new_assignment UNIQUE (changeInterface, oldInterface, operator),
  CONSTRAINT type_status_assignment CHECK (statusAssignment IN ('PENDING', 'INSPECTED', 'REDISCOVERED'))
);