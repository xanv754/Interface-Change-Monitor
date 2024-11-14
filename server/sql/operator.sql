CREATE TABLE operator (
    username VARCHAR(20) PRIMARY KEY,
    name VARCHAR(30) NOT NULL, 
    lastname VARCHAR(30) NOT NULL,
    password VARCHAR(64) NOT NULL,
	role VARCHAR(8) NOT NULL,
	status VARCHAR(8) NOT NULL,
    CONSTRAINT type_role CHECK (role IN ('ADMIN', 'STANDARD')),
    CONSTRAINT status_account CHECK (status IN ('ACTIVE', 'INACTIVE'))
);

INSERT INTO operator (username, name, lastname, password, role, status)
VALUES
  ('admin', 'John', 'Doe', 'password123', 'ADMIN', 'ACTIVE'),
  ('user1', 'Jane', 'Smith', 'pass456', 'STANDARD', 'ACTIVE'),
  ('user2', 'Michael', 'Johnson', 'secret789', 'STANDARD', 'INACTIVE');
  ('user3', 'Manuel', 'Peterson', 'secret123', 'STANDARD', 'ACTIVE');