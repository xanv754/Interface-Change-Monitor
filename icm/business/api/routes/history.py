from typing import Annotated, Tuple
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from icm.business.libs.code import ResponseCode
from icm.business.controllers.assignment import AssignmentController
from icm.business.controllers.security import SecurityController
from icm.business.models.assignment import AssignmentModel
from icm.business.models.user import UserModel

router = APIRouter()


class StatusRequest(BaseModel):
    status: str


class MonthRequest(BaseModel):
    date: str
    usernames: list[str]


@router.post("/history/assignments", response_model=list[AssignmentModel])
def get_assignments(request: StatusRequest, user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Get assignments from a user by status."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    controller = AssignmentController()
    response: Tuple[ResponseCode, list] = controller.get_user_assignments_filter_by_status(username=user.username, status=request.status)
    if response[0].status == 200:
        return response[1]
    raise response[0].error

@router.get("/history/user", response_model=list[AssignmentModel])
def get_user_history(date: str, user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Get user history by a date (YYYY-MM)."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    controller = AssignmentController()
    response: Tuple[ResponseCode, list[dict]] = controller.get_user_assignments_completed_in_month(username=user.username, date=date)
    if response[0].status == 200:
        return response[1]
    raise response[0].error

@router.post("/history/all", response_model=list[AssignmentModel])
def get_all_history(request: MonthRequest, user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Get user histories by a date (YYYY-MM)."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    controller = AssignmentController()
    response: Tuple[ResponseCode, list[dict]] = controller.get_users_assignments_completed_in_month(usernames=request.usernames, date=request.date)
    if response[0].status == 200:
        return response[1]
    raise response[0].error

@router.get("/history/available", response_model=list)
def get_date_available_to_consult_history(user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """"""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    controller = AssignmentController()
    response: Tuple[ResponseCode, list[dict]] = controller.get_date_available_to_consult_history()
    if response[0].status == 200:
        return response[1]
    raise response[0].error