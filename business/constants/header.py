from constants.fields import InterfaceField, AssignmentField


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

HEADER_AUTOMATIC_ASSIGNMENT = [
    AssignmentField.OLD_INTERFACE_ID,
    AssignmentField.CURRENT_INTERFACE_ID,
    AssignmentField.USERNAME,
    AssignmentField.ASSIGN_BY,
    AssignmentField.TYPE_STATUS,
]