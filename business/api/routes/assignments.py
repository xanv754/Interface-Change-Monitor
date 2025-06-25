from typing import Annotated, Tuple
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from business.controllers.security import SecurityController
from business.libs.code import ResponseCode
from business.controllers.assignment import AssignmentController
from business.controllers.config import ConfigController
from business.models.user import UserModel
from business.models.assignment import StatisticsModel
from business.models.assignment import NewAssignmentModel, AssignmentModel


router = APIRouter()


class StatusRequest(BaseModel):
    status: str


class StatisticsRequest(BaseModel):
    usernames: list[str]


@router.post("/assignments/new", status_code=201)
def new_assignments(assignments: list[NewAssignmentModel], user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """New assignments."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    permission_request = ConfigController.can_assign_permission(role=user.role)
    if not permission_request:
        raise ResponseCode(status=403, message="User not authorized to assign").error
    controller = AssignmentController()
    response: ResponseCode = controller.new_assignment(assignments=assignments)
    if response.status == 201:
        return {"message": "Assignments created successfully"}
    raise response.error

@router.post("/assignments")
def get_assignments(request: StatusRequest, user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Get assignments from a user by status."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    controller = AssignmentController()
    response: Tuple[ResponseCode, list] = controller.get_all_assignments_filter_by_status(status=request.status)
    if response[0].status == 200:
        return response[1]
    raise response[0].error

@router.get("/assignments/statistics/user", response_model=list[StatisticsModel])
def get_assignments_statistics(user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Get assignments statistics from a user."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    controller = AssignmentController()
    response: Tuple[ResponseCode, list] = controller.get_statistics_assignments(usernames=[user.username])
    if response[0].status == 200:
        return response[1]
    raise response[0].error

@router.post("/assignments/statistics/all", response_model=list[StatisticsModel])
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