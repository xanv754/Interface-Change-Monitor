from typing import Tuple, List
from pandas import DataFrame
from icm.access import ChangeQuery
from icm.utils import OperationData, HEADER_RESPONSE_INTERFACES_CHANGES, log
from icm.business.libs.code import ResponseCode
from icm.business.models.change import UpdateChangeModel
from icm.constants.fields import ChangeField


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
            status_operation = ChangeController.delete_changes()
            if not status_operation: raise Exception()
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
            if data.empty: return ResponseCode(status=200), []
            data = OperationData.transform_to_json(data=data)
            return ResponseCode(status=200), data
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Change controller error. Failed to get interfaces with changes. {error}")
            return ResponseCode(status=500), []
        
    @staticmethod
    def update_assignment(changes: List[UpdateChangeModel]) -> ResponseCode:
        """Update assignment of changes.
        
        Parameters
        ----------
        changes : List[UpdateChangeModel]
            Data to update.
        """
        try:
            query = ChangeQuery()
            status_operation = query.update_assign(data=changes)
            if not status_operation: raise Exception()
            return ResponseCode(status=200)
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Change controller error. Failed to update assignment of changes. {error}")
            return ResponseCode(status=500)
        
    @staticmethod
    def delete_changes() -> bool:
        """Delete changes.
        
        Returns
        -------
        ResponseCode
            Response code.
        """
        try:
            query = ChangeQuery()
            status_operation = query.delete_changes()
            if not status_operation: raise Exception()
            return True
        except Exception as error:
            error = str(error).strip().capitalize()
            log.error(f"Change controller error. Failed to delete changes. {error}")
            return False