from database.models.equipment import EquipmentModel

if __name__ == "__main__":
    equipment = EquipmentModel.get_equipment(1)
    print(equipment)