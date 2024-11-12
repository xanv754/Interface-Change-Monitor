CREATE TABLE equip_inter (
    id SERIAL PRIMARY KEY,
    id_yesterday_interface SERIAL REFERENCES interface(id) ON DELETE CASCADE,
    id_today_interface SERIAL REFERENCES interface(id) ON DELETE CASCADE,
    id_equipment SERIAL REFERENCES equipment(id) ON DELETE CASCADE
);

INSERT INTO equip_inter (id_yesterday_interface, id_today_interface, id_equipment)
VALUES
  (1, 2, 1),
  (3, 3, 2);