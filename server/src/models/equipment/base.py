from abc import ABC
from queries.equipment.create import CreateEquipmentQuery
from queries.equipment.read import ReadEquipmentQuery
from queries.equipment.update import UpdateEquipmentQuery
from queries.equipment.delete import DeleteEquipmentQuery
from entities.equipment import EquipmentEntity
from models.equipment.model import EquipmentModel

class Equipment(CreateEquipmentQuery, ReadEquipmentQuery, UpdateEquipmentQuery, DeleteEquipmentQuery, ABC):

    def entity_to_model(self, equipment: EquipmentEntity) -> EquipmentModel:
        return EquipmentModel(
            id=equipment.id,
            ip=equipment.ip,
            community=equipment.community,
            sysname=equipment.sysname,
            createdat=equipment.createdat.strftime("%Y-%m-%d"),
            updatedat=(equipment.updatedat.strftime("%Y-%m-%d") if equipment.updatedat else None)
        )