from typing import Annotated, Tuple
from fastapi import APIRouter, Depends
from api.security.controller import SecurityController
from controllers.change import ChangeController
from controllers.config import ConfigController
from models.user import UserModel
from constants.code import ResponseCode

router = APIRouter()


@router.get("/changes")
def get_changes(user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Get interfaces with changes of the day."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    permission_request = ConfigController.can_assign_permission(role=user.role)
    if not permission_request:
        raise ResponseCode(status=403, message="User not authorized to get interface changes").error
    controller = ChangeController()
    response: Tuple[ResponseCode, list] = controller.get_interfaces_with_changes()
    if response[0].status == 200:
        return response[1]
    raise response[0].error
