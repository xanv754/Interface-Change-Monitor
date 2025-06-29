from typing import Annotated, Tuple
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from business.libs.code import ResponseCode
from business.controllers.assignment import AssignmentController
from business.controllers.security import SecurityController
from business.models.assignment import AssignmentModel
from business.models.user import UserModel

router = APIRouter()


class StatusRequest(BaseModel):
    status: str


class MonthRequest(BaseModel):
    month: str
    usernames: list[str]


@router.post("/history/assignments", response_model=list[AssignmentModel])
def get_assignments(request: StatusRequest, user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Get assignments from a user by status."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    controller = AssignmentController()
    response: Tuple[ResponseCode, list] = controller.get_all_assignments_filter_by_status(status=request.status)
    if response[0].status == 200:
        return response[1]
    raise response[0].error

@router.get("/history/user", response_model=list[AssignmentModel])
def get_user_history(month: int, user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Get user history."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    controller = AssignmentController()
    response: Tuple[ResponseCode, list[dict]] = controller.get_user_assignments_completed_in_month(username=user.username, month=month)
    if response[0].status == 200:
        return response[1]
    raise response[0].error

@router.post("/history/all", response_model=list[AssignmentModel])
def get_all_history(request: MonthRequest, user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Get user history."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    controller = AssignmentController()
    response: Tuple[ResponseCode, list[dict]] = controller.get_users_assignments_completed_in_month(usernames=request.usernames, month=request.month)
    if response[0].status == 200:
        return response[1]
    raise response[0].error
