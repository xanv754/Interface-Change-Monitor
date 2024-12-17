from entities.operator import OperatorEntity
from models.operator.model import OperatorModel

def operator_entity_to_model(operator_entity: OperatorEntity) -> OperatorModel:
    return OperatorModel(
        username=operator_entity.username,
        name=operator_entity.name,
        lastname=operator_entity.lastname,
        password=operator_entity.password,
        profile=operator_entity.profile.value,
        statusaccount=operator_entity.statusaccount.value,
        createdat=operator_entity.createdat.strftime("%Y-%m-%d")
    )