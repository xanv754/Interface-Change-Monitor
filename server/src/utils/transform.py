from typing import List
from schemas import (
    OperatorResponseSchema, 
    EquipmentResponseSchema, 
    InterfaceResponseSchema, 
    AssignmentResponseSchema, 
    AssignmentInterfaceResponseSchema,
    AssignmentStatisticsResponse
)


def operator_to_dict(operators_tuple: List[tuple]) -> List[OperatorResponseSchema]:
    """Transform a list of tuples to a list of OperatorSchema objects. \n
    _Note:_ The password is not returned.

    Parameters
    ----------
    operators_tuple : List[tuple]
        List of tuples with the data of the operators.
    """
    operators: List[OperatorResponseSchema] = []
    for res in operators_tuple:
        operators.append(
            OperatorResponseSchema(
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


def operator_complete_to_dict(operators_tuple: List[tuple]) -> List[OperatorResponseSchema]:
    """Transform a list of tuples to a list of OperatorSchema objects. \n
    _Note:_ The password is returned.

    Parameters
    ----------
    operators_tuple : List[tuple]
        List of tuples with the data of the operators.
    """
    operators: List[OperatorResponseSchema] = []
    for res in operators_tuple:
        operators.append(
            OperatorResponseSchema(
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


def equipment_to_dict(equipments_tuple: List[tuple]) -> List[EquipmentResponseSchema]:
    """Transform a list of tuples to a list of EquipmentSchema objects.

    Parameters
    ----------
    equipments_tuple : List[tuple]
        List of tuples with the data of the equipments.
    """
    equipments: List[EquipmentResponseSchema] = []
    for res in equipments_tuple:
        equipments.append(
            EquipmentResponseSchema(
                id=res[0],
                ip=res[1],
                community=res[2],
                sysname=res[3] if res[3] != None else None,
                createdAt=res[4].strftime("%Y-%m-%d"),
                updatedAt=(res[5].strftime("%Y-%m-%d") if res[5] != None else None),
            )
        )
    return equipments


def interface_to_dict(interfaces_tuple: List[tuple]) -> List[InterfaceResponseSchema]:
    """Transform a list of tuples to a list of InterfaceSchema objects.

    Parameters
    ----------
    interfaces_tuple : List[tuple]
        List of tuples with the data of the interfaces.
    """
    interfaces: List[InterfaceResponseSchema] = []
    for res in interfaces_tuple:
        interfaces.append(
            InterfaceResponseSchema(
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


def assignment_to_dict(assignments_tuple: List[tuple]) -> List[AssignmentResponseSchema]:
    """Transform a list of tuples to a list of AssignmentSchema objects.

    Parameters
    ----------
    assignments_tuple : List[tuple]
        List of tuples with the data of the assignments.
    """
    assignments: List[AssignmentResponseSchema] = []
    for res in assignments_tuple:
        assignments.append(
            AssignmentResponseSchema(
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

def assignment_interface_to_dict(assignments_tuple: List[tuple]) -> List[AssignmentInterfaceResponseSchema]:
    """Transform a list of tuples to a list of AssignmentInterfaceResponseSchema objects.

    Parameters
    ----------
    assignments_tuple : List[tuple]
        List of tuples with the data of the assignments.
    """
    assignments: List[AssignmentInterfaceResponseSchema] = []
    for res in assignments_tuple:
        assignments.append(
            AssignmentInterfaceResponseSchema(
                idAssignment=res[0],
                dateAssignment=res[1].strftime("%Y-%m-%d"),
                statusAssignment=res[2],
                assignedBy=res[3],
                updateAt=(res[4].strftime("%Y-%m-%d") if res[7] != None else None),
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

def assignment_statistics_to_dict(assignments_tuple: List[tuple]) -> List[AssignmentStatisticsResponse]:
    """Transform a list of tuples to a list of AssignmentInterfaceResponseSchema objects.

    Parameters
    ----------
    assignments_tuple : List[tuple]
        List of tuples with the data of the assignments.
    """
    statistics: List[AssignmentStatisticsResponse] = []
    for res in assignments_tuple:
        statistics.append(
            AssignmentStatisticsResponse(
                username=res[0],
                name=res[1],
                lastname=res[2],
                totalPending=res[3],
                totalRevised=res[4]
            )
        )
    return statistics

def format_ifStatus(value: str) -> str:
    """Format the ifAdminStatus or ifOperStatus of the interface."""
    if "(" in value:
        value = value.split("(")[0]
    value = value.upper()
    return value
