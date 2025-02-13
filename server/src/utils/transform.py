from typing import List
from schemas import OperatorSchema, EquipmentSchema, InterfaceSchema, AssignmentSchema


def operator_to_dict(operators_tuple: List[tuple]) -> List[OperatorSchema]:
    operators: List[OperatorSchema] = []
    for res in operators_tuple:
        operators.append(
            OperatorSchema(
                username=res[0],
                name=res[1],
                lastname=res[2],
                password="",
                profile=res[4],
                account=res[5],
                created_at=res[6].strftime("%Y-%m-%d"),
            )
        )
    return operators


def operator_complete_to_dict(operators_tuple: List[tuple]) -> List[OperatorSchema]:
    operators: List[OperatorSchema] = []
    for res in operators_tuple:
        operators.append(
            OperatorSchema(
                username=res[0],
                name=res[1],
                lastname=res[2],
                password=res[3],
                profile=res[4],
                account=res[5],
                created_at=res[6].strftime("%Y-%m-%d"),
            )
        )
    return operators


def equipment_to_dict(equipments_tuple: List[tuple]) -> List[EquipmentSchema]:
    equipments: List[EquipmentSchema] = []
    for res in equipments_tuple:
        equipments.append(
            EquipmentSchema(
                id=res[0],
                ip=res[1],
                community=res[2],
                sysname=res[3] if res[3] != None else None,
                created_at=res[4].strftime("%Y-%m-%d"),
                updated_at=(
                    res[5].strftime("%Y-%m-%d") if res[5] != None else None
                )
            )
        )
    return equipments


def interface_to_dict(interfaces_tuple: List[tuple]) -> List[InterfaceSchema]:
    interfaces: List[InterfaceSchema] = []
    for res in interfaces_tuple:
        interfaces.append(
            InterfaceSchema(
                id=res[0],
                equipment=res[2],
                date=res[3].strftime("%Y-%m-%d"),
                type=res[4],
                ifIndex=res[1],
                ifName=res[5],
                ifDescr=res[6],
                ifAlias=res[7],
                ifSpeed=res[8],
                ifHighSpeed=res[9],
                ifPhysAddress=res[10],
                ifType=res[11],
                ifOperStatus=res[12],
                ifAdminStatus=res[13],
                ifPromiscuousMode=res[14],
                ifConnectorPresent=res[15],
                ifLastCheck=res[16]
            )
        )
    return interfaces


def assignment_to_dict(assignments_tuple: List[tuple]) -> List[AssignmentSchema]:
    assignments: List[AssignmentSchema] = []
    for res in assignments_tuple:
        assignments.append(
            AssignmentSchema(
                id=res[0],
                new_interface=res[1],
                old_interface=res[2],
                operator=res[3],
                date=res[4].strftime("%Y-%m-%d"),
                status=res[5],
                assigned_by=res[6],
                updated_at=(
                    res[7].strftime("%Y-%m-%d") if res[7] != None else None
                )
            )
        )
    return assignments
