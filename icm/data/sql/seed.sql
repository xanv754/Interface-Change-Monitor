INSERT INTO users (username, password, name, lastname, status, role) VALUES
('admin_root', 'hash_password_123', 'Sistema', 'Administrador', 'ACTIVE', 'ROOT'),
('test', 'hash_password_456', 'Juan', 'Perez', 'ACTIVE', 'USER'),
('soporte_tech', 'hash_password_789', 'Ana', 'Gomez', 'ACTIVE', 'SOPORT'),
('user_old', 'hash_password_000', 'Pedro', 'Duran', 'INACTIVE', 'USER');

INSERT INTO interfaces (ip, community, sysname, ifindex, ifname, ifdescr, ifalias, ifhighspeed, ifoperstatus, ifadminstatus, consulted_at) VALUES
('10.0.0.1', 'public', 'Core-SW-01', 1, 'Gig0/1', 'Link to Server', 'SRV-01', '1000', 'up', 'up', CURRENT_DATE - INTERVAL '2 days'),
('10.0.0.1', 'public', 'Core-SW-01', 2, 'Gig0/2', 'Link to Firewall', 'FW-01', '1000', 'down', 'up', CURRENT_DATE - INTERVAL '2 days'),
('192.168.1.50', 'private', 'Edge-Router', 10, 'Eth1', 'ISP Link', 'WAN', '100', 'up', 'up', CURRENT_DATE - INTERVAL '2 days'),
('10.0.0.1', 'public', 'Core-SW-01', 1, 'Gig0/1', 'Link to Server', 'SRV-01-UPDATED', '1000', 'up', 'up', CURRENT_DATE),
('10.0.0.1', 'public', 'Core-SW-01', 2, 'Gig0/2', 'Link to Firewall', 'FW-01', '1000', 'up', 'up', CURRENT_DATE),
('192.168.1.50', 'private', 'Edge-Router', 10, 'Eth1', 'ISP Link', 'WAN', '100', 'down', 'up', CURRENT_DATE);

INSERT INTO changes (id_old, ip_old, community_old, sysname_old, ifindex_old, id_new, ip_new, community_new, sysname_new, ifindex_new, assigned)
SELECT 
    i1.id, i1.ip, i1.community, i1.sysname, i1.ifindex::text,
    i2.id, i2.ip, i2.community, i2.sysname, i2.ifindex::text,
    'PENDING'
FROM interfaces i1, interfaces i2
WHERE i1.ip = i2.ip AND i1.ifindex = i2.ifindex 
AND i1.consulted_at < i2.consulted_at;

INSERT INTO assignments (old_interface_id, current_interface_id, user_id, assign_by, type_status)
SELECT 
    c.id_old, 
    c.id_new, 
    'test', 
    'admin_root', 
    'PENDING'
FROM changes c
LIMIT 2;

INSERT INTO assignments (old_interface_id, current_interface_id, user_id, assign_by, type_status)
SELECT 
    c.id_old, 
    c.id_new, 
    'soporte_tech', 
    'admin_root', 
    'INSPECTED'
FROM changes c
OFFSET 2 LIMIT 1;
