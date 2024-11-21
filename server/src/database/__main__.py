import traceback
from database.models.equipment import EquipmentModel
from database.models.operator import OperatorModel
from database.models.interface import InterfaceModel
from database.models.assignment import AssignmentModel
from database.utils.json import interface_to_json, equipment_to_json, assignment_to_json, operator_to_json

if __name__ == "__main__":
    try:
        equipment = EquipmentModel.get_equipment_by_id(1)
        res = equipment_to_json([equipment])
        print(res)
        interface = InterfaceModel.get_interface_by_id(1)
        res = interface_to_json([interface])
        print(res)
        operator = OperatorModel.get_operator('user1')
        res = operator_to_json([operator])
        print(res)
        assignment = AssignmentModel.get_assignment(2, 1, 'user1')
        res = assignment_to_json([assignment])
        print(res)
    except:
        traceback.print_exc()