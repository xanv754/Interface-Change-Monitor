from typing import Tuple
from fastapi import APIRouter
from controllers.change import ChangeController
from constants.code import ResponseCode

router = APIRouter()


@router.get("/changes")
def get_changes():
    """Get interfaces with changes of the day."""
    controller = ChangeController()
    response: Tuple[ResponseCode, list] = controller.get_interfaces_with_changes()
    if response[0].status == 200:
        return response[1]
    raise response[0].error
