from entity.interface import Interface
from typing import List

def create_data(interfaces: List[dict]) -> List[Interface]:
    new_interfaces: List[Interface] = []
    for interface in interfaces:
        try:
            if 'ip' in interface: ip = interface['ip']
            else: ip = None
            if 'community' in interface: community = interface['community']
            else: community = None
            if 'ifIndex' in interface: ifIndex = interface['ifIndex']
            else: ifIndex = None
            if ip and community and ifIndex:
                if ('ifName' in interface) and (interface['ifName'] != ""): ifName = interface['ifName']
                else: ifName = "STRING:"
                if ('ifDescr' in interface) and (interface['ifDescr'] != ""): ifDescr = interface['ifDescr']
                else: ifDescr = "STRING:"
                if ('ifAlias' in interface) and (interface['ifAlias'] != ""): ifAlias = interface['ifAlias']
                else: ifAlias = "STRING:"
                if ('ifHighSpeed' in interface) and (interface['ifHighSpeed'] != ""): ifHighSpeed = interface['ifHighSpeed']
                else: ifHighSpeed = "Gauge32:"
                if ('ifOperStatus' in interface) and (interface['ifOperStatus'] != ""): ifOperStatus = interface['ifOperStatus']
                else: ifOperStatus = "INTEGER:"
                if ('ifAdminStatus' in interface) and (interface['ifAdminStatus'] != ""): ifAdminStatus = interface['ifAdminStatus']
                else: ifAdminStatus = "INTEGER:"
                new_interface = Interface(ip=ip, community=community, ifIndex=ifIndex, ifName=ifName, ifDescr=ifDescr, ifAlias=ifAlias, ifHighSpeed=ifHighSpeed, ifOperStatus=ifOperStatus, ifAdminStatus=ifAdminStatus)
                new_interfaces.append(new_interface)
            else: continue
        except Exception as e:
            print(e)
            return None
    return new_interfaces

def lower_data(data: dict) -> dict:
    new_data = {}
    for key, value in data.items():
        if type(value) == str:
            new_value = value.lower()
            new_data[key] = new_value
        else:
            new_data[key] = value
    return new_data