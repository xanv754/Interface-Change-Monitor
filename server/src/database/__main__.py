import traceback
from database.models.equipment import EquipmentModel
from database.models.operator import OperatorModel
from database.models.interface import InterfaceModel
from database.models.assignment import AssignmentModel

if __name__ == "__main__":
    try:
        equipment = EquipmentModel.get_equipment_by_id(1)
        print(equipment)
        operator = OperatorModel.get_operator('user')
        print(operator)
        interface = InterfaceModel.get_interface_by_id(1)
        print(interface)
        assignment = AssignmentModel.get_assignment(2, 1, 'user1')
        print(assignment)
        print(assignment.model_dump())
    except:
        traceback.print_exc()