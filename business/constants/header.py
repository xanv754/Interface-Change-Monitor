from constants.fields import InterfaceField


HEADER_CONSULT_SNMP = [
    InterfaceField.IP,
    InterfaceField.COMMUNITY,
    InterfaceField.SYSNAME,
    InterfaceField.IFINDEX,
    InterfaceField.IFNAME,
    InterfaceField.IFDESCR,
    InterfaceField.IFALIAS,
    InterfaceField.IFHIGHSPEED,
    InterfaceField.IFOPERSTATUS,
    InterfaceField.IFADMINSTATUS,
    InterfaceField.CONSULTED_AT
]


HEADER_RESPONSE_INTERFACES = [
    InterfaceField.ID,
    InterfaceField.IP,
    InterfaceField.COMMUNITY,
    InterfaceField.SYSNAME,
    InterfaceField.IFINDEX,
    InterfaceField.IFNAME,
    InterfaceField.IFDESCR,
    InterfaceField.IFALIAS,
    InterfaceField.IFHIGHSPEED,
    InterfaceField.IFOPERSTATUS,
    InterfaceField.IFADMINSTATUS,
    InterfaceField.CONSULTED_AT
]