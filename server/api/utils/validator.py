from entity.interface import Interface
from models.snmp import snmp

def change_validator(interface: Interface, backup: Interface) -> bool:
    """Detect if two objects have differences.

    Parameters
    ----------
        interface (Interface): Last data interface.
        backup (Interface): Backup data interface.
        
    Returns
    ------
        True: they are different; False: they are same. 
    """
    if (interface.ifName != snmp["ifName"]) and (interface.ifName != backup.ifName): return True
    if (interface.ifDescr != snmp["ifDescr"]) and (interface.ifDescr != backup.ifDescr): return True
    if (interface.ifAlias != snmp["ifAlias"]) and (interface.ifAlias != backup.ifAlias): return True
    if (interface.ifHighSpeed != snmp["ifHighSpeed"]) and (interface.ifHighSpeed != backup.ifHighSpeed): return True
    if (interface.ifOperStatus != snmp["ifOperStatus"]) and (interface.ifOperStatus != backup.ifOperStatus): return True
    if (interface.ifAdminStatus != snmp["ifAdminStatus"]) and (interface.ifAdminStatus != backup.ifAdminStatus): return True
    return False
