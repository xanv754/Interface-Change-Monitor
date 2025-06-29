from typing import Annotated, Tuple
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from business.libs.code import ResponseCode
from business.controllers.assignment import AssignmentController
from business.controllers.config import ConfigController
from business.controllers.security import SecurityController
from business.models.user import UserModel
from business.models.assignment import StatisticsModel


router = APIRouter()


class StatisticsRequest(BaseModel):
    usernames: list[str]


@router.get("/statistics/assignments/user", response_model=StatisticsModel)
def get_assignments_statistics(user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Get assignments statistics from a user."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    controller = AssignmentController()
    response: Tuple[ResponseCode, list] = controller.get_statistics_assignments(usernames=[user.username])
    if response[0].status == 200:
        if response[1]: return response[1][0]
        return {}
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