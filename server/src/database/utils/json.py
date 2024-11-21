from typing import List
from database.entities.interface import InterfaceEntity
from database.entities.assignment import AssignmentEntity
from database.entities.operator import OperatorEntity
from database.entities.equipment import EquipmentEntity

def interface_to_json(interfaces: List[InterfaceEntity]) -> list:
    """Convert a list of interfaces to a JSON object list.
    
    Parameters
    ----------
    interfaces : List[InterfaceEntity]
        The list of interfaces to be converted.
    """
    json_interfaces = []
    for interface in interfaces:
        json_interfaces.append({
            "id": interface.id,
            "ifIndex": interface.ifIndex,
            "idEquipment": interface.idEquipment,
            "dateConsult": interface.dateConsult.strftime("%Y-%m-%d"),
            "dateType": interface.dateType.value,
            "ifName": interface.ifName,
            "ifDescr": interface.ifDescr,
            "ifAlias": interface.ifAlias,
            "ifSpeed": interface.ifSpeed,
            "ifHighSpeed": interface.ifHighSpeed,
            "ifPhysAddress": interface.ifPhysAddress,
            "ifType": interface.ifType,
            "ifOperStatus": interface.ifOperStatus.value,
            "ifAdminStatus": interface.ifAdminStatus.value,
            "ifPromiscuousMode": interface.ifPromiscuousMode,
            "ifConnectorPresent": interface.ifConnectorPresent,
            "ifLastCheck": interface.ifLastCheck
        })
    return json_interfaces

def assignment_to_json(assignments: List[AssignmentEntity]) -> list:
    """Convert a list of assignments to a JSON object list.
    
    Parameters
    ----------
    assignments : List[AssignmentEntity]
        The list of assignments to be converted.
    """
    json_assignments = []
    for assignment in assignments:
        json_assignments.append({
            "changeInterface": assignment.changeInterface,
            "oldInterface": assignment.oldInterface,
            "operator": assignment.operator,
            "dateAssignment": assignment.dateAssignment.strftime("%Y-%m-%d"),
            "statusAssignment": assignment.statusAssignment.value,
            "assignedBy": assignment.assignedBy,
            "dateReview": assignment.dateReview.strftime("%Y-%m-%d") if assignment.dateReview else None
        })
    return json_assignments

def operator_to_json(operators: List[OperatorEntity]) -> list:
    """Convert a list of operators to a JSON object list.
    
    Parameters
    ----------
    operators : List[OperatorEntity]
        The list of operators to be converted.
    """
    json_operators = []
    for operator in operators:
        json_operators.append({
            "username": operator.username,
            "name": operator.name,
            "lastname": operator.lastname,
            "password": operator.password,
            "profile": operator.profile.value,
            "statusAccount": operator.statusAccount.value,
            "deleteOperator": operator.deleteOperator
        })
    return json_operators

def equipment_to_json(equipments: List[EquipmentEntity]) -> list:
    """Convert a list of equipments to a JSON object list.
    
    Parameters
    ----------
    equipments : List[EquipmentEntity]
        The list of equipments to be converted.
    """
    json_equipments = []
    for equipment in equipments:
        json_equipments.append({
            "id": equipment.id,
            "ip": equipment.ip,
            "community": equipment.community,
            "sysname": equipment.sysname,
            "createdAt": equipment.createdAt.strftime("%Y-%m-%d"),
            "updatedAt": equipment.updatedAt.strftime("%Y-%m-%d") if equipment.updatedAt else None
        })
    return json_equipments