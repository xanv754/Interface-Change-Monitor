CREATE TABLE interface (
    id SERIAL PRIMARY KEY,
    index numeric(10) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description VARCHAR(200) NOT NULL,
    alias VARCHAR(200) NOT NULL,
    high_speed numeric(10) NOT NULL,
    status_operator VARCHAR(4) NOT NULL,
    status_administration VARCHAR(4) NOT NULL,
    last_check date NOT NULL
    CONSTRAINT type_status_operator CHECK (status_operator IN ('UP', 'DOWN')),
    CONSTRAINT type_status_administration CHECK (status_administration IN ('UP', 'DOWN'))
);

INSERT INTO interface (index, name, description, alias, high_speed, status_operator, status_administration, last_check)
VALUES
  (1, 'GigabitEthernet0/1', 'Interface 1', 'GE0/1', 1000, 'UP', 'UP', '2023-11-12'),
  (2, 'FastEthernet0/2', 'Interface 2', 'FE0/2', 100, 'DOWN', 'UP', '2023-11-11'),
  (3, 'Serial0/0', 'Serial Interface', 'S0/0', 2000, 'UP', 'UP', '2023-11-12');

DELETE FROM interface WHERE id = 3;