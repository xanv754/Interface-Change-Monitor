from typing import List
from schemas import (
    OperatorSchema, 
    EquipmentSchema, 
    InterfaceSchema, 
    AssignmentSchema, 
    AssignmentInterfaceSchema,
    AssignmentInterfaceAssignedSchema,
    AssignmentStatisticsSchema,
    ChangeInterfaceSchema
)


def operator_to_dict(operators_tuple: List[tuple]) -> List[OperatorSchema]:
    """Transform a list of tuples to a list of OperatorSchema objects. \n
    _Note:_ The password is not returned.

    Parameters
    ----------
    operators_tuple : List[tuple]
        List of tuples with the data of the operators.
    """
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
                createdAt=res[6].strftime("%Y-%m-%d"),
            )
        )
    return operators


def operator_complete_to_dict(operators_tuple: List[tuple]) -> List[OperatorSchema]:
    """Transform a list of tuples to a list of OperatorSchema objects. \n
    _Note:_ The password is returned.

    Parameters
    ----------
    operators_tuple : List[tuple]
        List of tuples with the data of the operators.
    """
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
                createdAt=res[6].strftime("%Y-%m-%d"),
            )
        )
    return operators


def equipment_to_dict(equipments_tuple: List[tuple]) -> List[EquipmentSchema]:
    """Transform a list of tuples to a list of EquipmentSchema objects.

    Parameters
    ----------
    equipments_tuple : List[tuple]
        List of tuples with the data of the equipments.
    """
    equipments: List[EquipmentSchema] = []
    for res in equipments_tuple:
        equipments.append(
            EquipmentSchema(
                id=res[0],
                ip=res[1],
                community=res[2],
                sysname=res[3] if res[3] != None else None,
                createdAt=res[4].strftime("%Y-%m-%d"),
                updatedAt=(res[5].strftime("%Y-%m-%d") if res[5] != None else None),
            )
        )
    return equipments


def interface_to_dict(interfaces_tuple: List[tuple]) -> List[InterfaceSchema]:
    """Transform a list of tuples to a list of InterfaceSchema objects.

    Parameters
    ----------
    interfaces_tuple : List[tuple]
        List of tuples with the data of the interfaces.
    """
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
                ifHighSpeed=res[8],
                ifOperStatus=res[9],
                ifAdminStatus=res[10]
            )
        )
    return interfaces


def assignment_to_dict(assignments_tuple: List[tuple]) -> List[AssignmentSchema]:
    """Transform a list of tuples to a list of AssignmentSchema objects.

    Parameters
    ----------
    assignments_tuple : List[tuple]
        List of tuples with the data of the assignments.
    """
    assignments: List[AssignmentSchema] = []
    for res in assignments_tuple:
        assignments.append(
            AssignmentSchema(
                id=res[0],
                newInterface=res[1],
                oldInterface=res[2],
                operator=res[3],
                date=res[4].strftime("%Y-%m-%d"),
                status=res[5],
                assignedBy=res[6],
                updatedAt=(res[7].strftime("%Y-%m-%d") if res[7] != None else None),
            )
        )
    return assignments

def assignment_interface_to_dict(assignments_tuple: List[tuple]) -> List[AssignmentInterfaceSchema]:
    """Transform a list of tuples to a list of AssignmentInterfaceResponseSchema objects.

    Parameters
    ----------
    assignments_tuple : List[tuple]
        List of tuples with the data of the assignments.
    """
    assignments: List[AssignmentInterfaceSchema] = []
    for res in assignments_tuple:
        assignments.append(
            AssignmentInterfaceSchema(
                idAssignment=res[0],
                dateAssignment=res[1].strftime("%Y-%m-%d"),
                statusAssignment=res[2],
                assignedBy=res[3],
                updateAt=(res[4].strftime("%Y-%m-%d") if res[4] != None else None),
                oldIfName=res[5],
                oldIfDescr=res[6],
                oldIfAlias=res[7],
                oldIfHighSpeed=res[8],
                oldIfOperStatus=res[9],
                oldIfAdminStatus=res[10],
                newIfName=res[11],
                newIfDescr=res[12],
                newIfAlias=res[13],
                newIfHighSpeed=res[14],
                newIfOperStatus=res[15],
                newIfAdminStatus=res[16],
                ip=res[17],
                community=res[18],
                sysname=res[19],
                ifIndex=res[20]
            )
        )
    return assignments

def assignment_interface_assigned_to_dict(assignments_tuple: List[tuple]) -> List[AssignmentInterfaceAssignedSchema]:
    """Transform a list of tuples to a list of AssignmentInterfaceAssignedResponseSchema objects.

    Parameters
    ----------
    assignments_tuple : List[tuple]
        List of tuples with the data of the assignments.
    """
    assignments: List[AssignmentInterfaceAssignedSchema] = []
    for res in assignments_tuple:
        assignments.append(
            AssignmentInterfaceAssignedSchema(
                idAssignment=res[0],
                dateAssignment=res[1].strftime("%Y-%m-%d"),
                statusAssignment=res[2],
                assignedBy=res[3],
                updateAt=(res[4].strftime("%Y-%m-%d") if res[4] != None else None),
                oldIfName=res[5],
                oldIfDescr=res[6],
                oldIfAlias=res[7],
                oldIfHighSpeed=res[8],
                oldIfOperStatus=res[9],
                oldIfAdminStatus=res[10],
                newIfName=res[11],
                newIfDescr=res[12],
                newIfAlias=res[13],
                newIfHighSpeed=res[14],
                newIfOperStatus=res[15],
                newIfAdminStatus=res[16],
                ip=res[17],
                community=res[18],
                sysname=res[19],
                ifIndex=res[20],
                username=(res[21] if res[21] != None else None),
                name=(res[22] if res[22] != None else None),
                lastname=(res[23] if res[23] != None else None)
            )
        )
    return assignments

def assignment_statistics_to_dict(assignments_tuple: List[tuple]) -> List[AssignmentStatisticsSchema]:
    """Transform a list of tuples to a list of AssignmentInterfaceResponseSchema objects.

    Parameters
    ----------
    assignments_tuple : List[tuple]
        List of tuples with the data of the assignments.
    """
    statistics: List[AssignmentStatisticsSchema] = []
    for res in assignments_tuple:
        statistics.append(
            AssignmentStatisticsSchema(
                username=res[0],
                name=res[1],
                lastname=res[2],
                totalPending=res[3],
                totalRevised=res[4]
            )
        )
    return statistics

def change_to_dict(changes_tuple: List[tuple]) -> List[ChangeInterfaceSchema]:
    """Transform a list of tuples to a list of ChangeInterfaceSchema objects.

    Parameters
    ----------
    changes_tuple : List[tuple]
        List of tuples with the data of the changes.
    """
    changes: List[ChangeInterfaceSchema] = []
    for res in changes_tuple:
        changes.append(
            ChangeInterfaceSchema(
                id=res[0],
                ip=res[1],
                community=res[2],
                sysname=res[3],
                ifIndex=res[4],
                newInterface=InterfaceSchema(
                    id=res[5],
                    equipment=res[6],
                    date=res[7].strftime("%Y-%m-%d"),
                    type=res[8],
                    ifIndex=res[4],
                    ifName=res[9],
                    ifDescr=res[10],
                    ifAlias=res[11],
                    ifHighSpeed=res[12],
                    ifOperStatus=res[13],
                    ifAdminStatus=res[14],
                ),
                oldInterface=InterfaceSchema(
                    id=res[15],
                    equipment=res[16],
                    date=res[17].strftime("%Y-%m-%d"),
                    type=res[18],
                    ifIndex=res[4],
                    ifName=res[19],
                    ifDescr=res[20],
                    ifAlias=res[21],
                    ifHighSpeed=res[22],
                    ifOperStatus=res[23],
                    ifAdminStatus=res[24],
                ),
                operator=(res[25] if res[25] != None else None)
            )
        )
    return changes

def format_ifStatus(value: str) -> str:
    """Format the ifAdminStatus or ifOperStatus of the interface."""
    if "(" in value:
        value = value.split("(")[0].strip()
    value = value.upper()
    return value
