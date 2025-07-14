from typing import Annotated, Tuple
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from icm.business.libs.code import ResponseCode
from icm.business.controllers.assignment import AssignmentController
from icm.business.controllers.config import ConfigController
from icm.business.controllers.security import SecurityController
from icm.business.models.user import UserModel
from icm.business.models.assignment import StatisticsModel


router = APIRouter()


class StatisticsRequest(BaseModel):
    usernames: list[str]


@router.get("/statistics/assignments/user", response_model=list[StatisticsModel])
def get_assignments_statistics(user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Get assignments statistics from a user."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    controller = AssignmentController()
    response: Tuple[ResponseCode, list] = controller.get_statistics_assignments(usernames=[user.username])
    if response[0].status == 200:
        return response[1]
    raise response[0].error

@router.post("/statistics/assignments/all", response_model=list[StatisticsModel])
def get_all_assignments_statistics(request: StatisticsRequest, user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Get all assignments statistics."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    permission_request = ConfigController.can_view_information_global_permission(role=user.role)
    if not permission_request:
        raise ResponseCode(status=403, message="User not authorized to get assignments statistics").error
    controller = AssignmentController()
    response: Tuple[ResponseCode, list] = controller.get_statistics_assignments(usernames=request.usernames)
    if response[0].status == 200:
        return response[1]
    raise response[0].error