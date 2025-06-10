from typing import Tuple, List
from datetime import datetime, timedelta
from pandas import DataFrame
from constants.header import HEADER_RESPONSE_INTERFACES_CHANGES
from constants.code import ResponseCode
from database.querys.change import ChangeQuery
from models.change import ChangeField
from utils.operation import OperationData
from utils.validate import Validate
from utils.log import log


class ChangeController:
    """Class to manage change controller."""

    @staticmethod
    def new_interfaces(data: DataFrame) -> ResponseCode:
        """Insert a new interface.
        
        Parameters
        ----------
        data : DataFrame
            Data with information of interfaces with their changes.
        """
        try:
            query = ChangeQuery()
            header_data = data.columns.tolist()
            if not header_data == HEADER_RESPONSE_INTERFACES_CHANGES:
                return ResponseCode(status=400, message="Invalid header of data interfaces with changes to insert") 
            data[ChangeField.ASSIGNED] = None
            buffer = OperationData.transform_to_buffer(data)
            status_operation = query.insert(data=buffer)
            if not status_operation: raise Exception()
            return ResponseCode(status=201)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Change controller error. Failed to insert a new interfaces with changes. {error}")
            return ResponseCode(status=500)
        
    @staticmethod
    def get_interfaces_with_changes() -> Tuple[ResponseCode, List[dict]]:
        """Get interfaces with changes.
        
        Returns
        -------
        Tuple[ResponseCode, DataFrame]
            Response code and a list of interfaces with changes.
        """
        try:
            query = ChangeQuery()
            data = query.get_all()
            if not data:
                return ResponseCode(status=404, message="Interfaces not found with changes"), []
            data = OperationData.transform_to_json(data=data)
            return ResponseCode(status=200), data
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Change controller error. Failed to get interfaces with changes. {error}")
            return ResponseCode(status=500), []