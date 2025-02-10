from typing import List
from constants import OperatorFields, EquipmentFields, InterfaceFields

def operator_to_dict(operators_tuple: List[tuple]) -> List[dict]:
    operators: List[dict] = []
    for res in operators_tuple:
        operators.append(
            {
                OperatorFields.USERNAME.value: res[0],
                OperatorFields.NAME.value: res[1],
                OperatorFields.LASTNAME.value: res[2],
                OperatorFields.PROFILE.value: res[4],
                OperatorFields.STATUS_ACCOUNT.value: res[5],
                OperatorFields.CREATED_AT.value: res[6].strftime("%Y-%m-%d"),
            }
        )
    return operators

def equipment_to_dict(equipments_tuple: List[tuple]) -> List[dict]:
    equipments: List[dict] = []
    for res in equipments_tuple:
        equipments.append(
            {
                EquipmentFields.ID.value: res[0],
                EquipmentFields.IP.value: res[1],
                EquipmentFields.COMMUNITY.value: res[2],
                EquipmentFields.SYSNAME.value: res[3],
                EquipmentFields.CREATED_AT.value: res[4].strftime("%Y-%m-%d"),
                EquipmentFields.UPDATED_AT.value: (
                    res[5].strftime("%Y-%m-%d") if res[5] != None else None
                ),
            }
        )
    return equipments

def interface_to_dict(interfaces_tuple: List[tuple]) -> List[dict]:
    interfaces: List[dict] = []
    for res in interfaces_tuple:
        interfaces.append(
            {
                InterfaceFields.ID.value: res[0],
                InterfaceFields.IFINDEX.value: res[1],
                InterfaceFields.IDEQUIPMENT.value: res[2],
                InterfaceFields.DATE_CONSULT.value: res[3].strftime("%Y-%m-%d"),
                InterfaceFields.IFNAME.value: res[4],
                InterfaceFields.IFDESCR.value: res[5],
                InterfaceFields.IFALIAS.value: res[6],
                InterfaceFields.IFSPEED.value: res[7],
                InterfaceFields.IFHIGHSPEED.value: res[8],
                InterfaceFields.IFPHYSADDRESS.value: res[9],
                InterfaceFields.IFTYPE.value: res[10],
                InterfaceFields.IFOPERSTATUS.value: res[11],
                InterfaceFields.IFADMINSTATUS.value: res[12],
                InterfaceFields.IFPROMISCUOUSMODE.value: res[13],
                InterfaceFields.IFCONNECTORPRESENT.value: res[14],
                InterfaceFields.IFLASTCHECK.value: res[15]
            }
        )
    return interfaces