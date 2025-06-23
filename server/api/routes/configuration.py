from typing import Annotated
from fastapi import APIRouter, Depends
from api.security.controller import SecurityController
from constants.types import RoleTypes
from controllers.config import ConfigController
from models.user import UserModel
from constants.code import ResponseCode


router = APIRouter()


@router.get("/configuration")
def get_changes(user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Get interfaces with changes of the day."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    if user.role != RoleTypes.ROOT:
        raise ResponseCode(status=403, message="User not authorized").error
    controller = ConfigController()
    response = controller.get_config()
    if response:
        return response.model_dump()
    else:
        raise ResponseCode(status=500, message="Error getting configuration").error
