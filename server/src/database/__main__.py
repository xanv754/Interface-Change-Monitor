import traceback
from database.models.equipment import EquipmentModel
from database.models.operator import OperatorModel
from database.models.interface import InterfaceModel
from database.models.assignment import AssignmentModel
from database.utils.json import interface_to_json, equipment_to_json, assignment_to_json, operator_to_json

if __name__ == "__main__":
    try:
        operators = OperatorModel.get_operators()
        res = operator_to_json(operators)
        print(res)
        equipments = EquipmentModel.get_equipments()
        res = equipment_to_json(equipments)
        print(res)
        interfaces = InterfaceModel.get_interfaces()
        res = interface_to_json(interfaces)
        print(res)
        assignments = AssignmentModel.get_assignments()
        res = assignment_to_json(assignments)
        print(res)
    except:
        traceback.print_exc()