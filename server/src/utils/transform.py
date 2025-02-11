from typing import List
from schemas import OperatorSchema, EquipmentSchema, InterfaceSchema, AssignmentSchema


def operator_to_dict(operators_tuple: List[tuple]) -> List[dict]:
    operators: List[dict] = []
    for res in operators_tuple:
        operators.append(
            {
                OperatorSchema.USERNAME.value: res[0],
                OperatorSchema.NAME.value: res[1],
                OperatorSchema.LASTNAME.value: res[2],
                OperatorSchema.PROFILE.value: res[4],
                OperatorSchema.STATUS_ACCOUNT.value: res[5],
                OperatorSchema.CREATED_AT.value: res[6].strftime("%Y-%m-%d"),
            }
        )
    return operators


def equipment_to_dict(equipments_tuple: List[tuple]) -> List[dict]:
    equipments: List[dict] = []
    for res in equipments_tuple:
        equipments.append(
            {
                EquipmentSchema.ID.value: res[0],
                EquipmentSchema.IP.value: res[1],
                EquipmentSchema.COMMUNITY.value: res[2],
                EquipmentSchema.SYSNAME.value: res[3],
                EquipmentSchema.CREATED_AT.value: res[4].strftime("%Y-%m-%d"),
                EquipmentSchema.UPDATED_AT.value: (
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
                InterfaceSchema.ID.value: res[0],
                InterfaceSchema.IFINDEX.value: res[1],
                InterfaceSchema.ID_EQUIPMENT.value: res[2],
                InterfaceSchema.DATE_CONSULT.value: res[3].strftime("%Y-%m-%d"),
                InterfaceSchema.IFNAME.value: res[4],
                InterfaceSchema.IFDESCR.value: res[5],
                InterfaceSchema.IFALIAS.value: res[6],
                InterfaceSchema.IFSPEED.value: res[7],
                InterfaceSchema.IFHIGHSPEED.value: res[8],
                InterfaceSchema.IFPHYSADDRESS.value: res[9],
                InterfaceSchema.IFTYPE.value: res[10],
                InterfaceSchema.IFOPERSTATUS.value: res[11],
                InterfaceSchema.IFADMINSTATUS.value: res[12],
                InterfaceSchema.IFPROMISCUOUSMODE.value: res[13],
                InterfaceSchema.IFCONNECTORPRESENT.value: res[14],
                InterfaceSchema.IFLASTCHECK.value: res[15],
            }
        )
    return interfaces


def assignment_to_dict(assignments_tuple: List[tuple]) -> List[dict]:
    assignments: List[dict] = []
    for res in assignments_tuple:
        assignments.append(
            {
                AssignmentSchema.ID.value: res[0],
                AssignmentSchema.CHANGE_INTERFACE.value: res[1],
                AssignmentSchema.OLD_INTERFACE.value: res[2],
                AssignmentSchema.OPERATOR.value: res[3],
                AssignmentSchema.DATE_ASSIGNMENT.value: res[4].strftime("%Y-%m-%d"),
                AssignmentSchema.STATUS_ASSIGNMENT.value: res[5],
                AssignmentSchema.ASSIGNED_BY.value: res[6],
                AssignmentSchema.UPDATED_AT.value: (
                    res[7].strftime("%Y-%m-%d") if res[7] != None else None
                ),
            }
        )
    return assignments
