from typing import Annotated
from fastapi import APIRouter, Depends
from business.libs.code import ResponseCode
from business.controllers.config import ConfigController
from business.controllers.security import SecurityController
from business.models.configuration import NewConfigModel
from business.models.user import UserModel
from constants.types import RoleTypes


router = APIRouter()


@router.get("/configuration")
def get_configuration(user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Get configuration of the system."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    permission_request = ConfigController.can_assign_permission(role=user.role)
    if not permission_request:
        raise ResponseCode(status=403, message="User not authorized").error
    controller = ConfigController()
    response = controller.get_config()
    if response:
        return response.model_dump()
    else:
        raise ResponseCode(status=500, message="Error getting configuration").error

@router.post("/configuration/new")
def new_configuration(new_config: NewConfigModel, user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Save new configuration."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    if user.role != RoleTypes.ROOT:
        raise ResponseCode(status=403, message="User not authorized").error
    controller = ConfigController()
    response = controller.new_config(new_config)
    if response.status == 200:
        return {"message": "Configuration saved successfully"}
    else:
        raise ResponseCode.error
