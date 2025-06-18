from models.interface import InterfaceField


SUFFIX_OLD = "_old"
SUFFIX_NEW = "_new"


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


HEADER_RESPONSE_INTERFACES_CHANGES = [
    InterfaceField.ID + SUFFIX_OLD,
    InterfaceField.IP + SUFFIX_OLD,
    InterfaceField.COMMUNITY + SUFFIX_OLD,
    InterfaceField.SYSNAME + SUFFIX_OLD,
    InterfaceField.IFINDEX + SUFFIX_OLD,
    InterfaceField.IFNAME + SUFFIX_OLD,
    InterfaceField.IFDESCR + SUFFIX_OLD,
    InterfaceField.IFALIAS + SUFFIX_OLD,
    InterfaceField.IFHIGHSPEED + SUFFIX_OLD,
    InterfaceField.IFOPERSTATUS + SUFFIX_OLD,
    InterfaceField.IFADMINSTATUS + SUFFIX_OLD,
    InterfaceField.ID + SUFFIX_NEW,
    InterfaceField.IP + SUFFIX_NEW,
    InterfaceField.COMMUNITY + SUFFIX_NEW,
    InterfaceField.SYSNAME + SUFFIX_NEW,
    InterfaceField.IFINDEX + SUFFIX_NEW,
    InterfaceField.IFNAME + SUFFIX_NEW,
    InterfaceField.IFDESCR + SUFFIX_NEW,
    InterfaceField.IFALIAS + SUFFIX_NEW,
    InterfaceField.IFHIGHSPEED + SUFFIX_NEW,
    InterfaceField.IFOPERSTATUS + SUFFIX_NEW,
    InterfaceField.IFADMINSTATUS + SUFFIX_NEW,
]