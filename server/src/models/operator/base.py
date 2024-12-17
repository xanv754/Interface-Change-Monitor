from abc import ABC
from queries.operator.create import CreateOperatorQuery
from queries.operator.read import ReadOperatorQuery
from queries.operator.update import UpdateOperatorQuery
from queries.operator.delete import DeleteOperatorQuery
from models.operator.model import OperatorModel
from entities.operator import OperatorEntity

class Operator(CreateOperatorQuery, ReadOperatorQuery, UpdateOperatorQuery, DeleteOperatorQuery, ABC):

    def entity_to_model(self, operator: OperatorEntity) -> OperatorModel:
        return OperatorModel(
            username=operator.username,
            name=operator.name,
            lastname=operator.lastname,
            password=operator.password,
            profile=operator.profile.value,
            statusaccount=operator.statusaccount.value,
            createdat=operator.createdat.strftime("%Y-%m-%d")
        )