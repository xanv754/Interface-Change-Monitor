CREATE TABLE assignment (
    id_equip_inter SERIAl REFERENCES equip_inter(id) ON DELETE CASCADE,
    id_operator VARCHAR(20) REFERENCES operator(username) ON DELETE CASCADE,
    CONSTRAINT id PRIMARY KEY (id_equip_inter, id_operator)
);

INSERT INTO assignment (id_equip_inter, id_operator)
VALUES
  (1, 'admin'),
  (2, 'user1');