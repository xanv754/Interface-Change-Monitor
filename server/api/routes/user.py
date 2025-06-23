from typing import Annotated, Tuple
from fastapi import APIRouter, Depends
from api.security.controller import SecurityController
from constants.code import ResponseCode
from controllers.user import UserController
from controllers.assignment import AssignmentController
from controllers.config import ConfigController
from models.user import UserModel, UserLoggedModel
from models.assignment import AssignmentCompleteModel


router = APIRouter()


@router.get("/user/info")
def get_user(user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Get user logged."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    controller = UserController()
    response: Tuple[ResponseCode, UserLoggedModel | None] = controller.get_user_logged(username=user.username)
    if response[0].status == 200:
        return response[1]
    raise response[0].error

@router.get("/user/all")
def get_users(user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Get all users active."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    permission_request = ConfigController.can_assign_permission(role=user.role)
    if not permission_request:
        raise ResponseCode(status=403, message="User not authorized to get users").error
    controller = UserController()
    response: Tuple[ResponseCode, list[UserModel]] = controller.get_users()
    if response[0].status == 200:
        if response[1]: return [user.model_dump(exclude={"password"}) for user in response[1]]
        return []
    raise response[0].error

@router.put("/user/info")
def update_user(new_user: UserModel, user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Update user."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    controller = UserController()
    response: ResponseCode = controller.update_user(user=new_user)
    if response.status == 200:
        return {"message": "User updated successfully"}
    raise response.error

@router.patch("/user/info/password")
def update_password(new_password: str, user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Update password of a user."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    controller = UserController()
    response: ResponseCode = controller.update_password(username=user.username, password=new_password)
    if response.status == 200:
        return {"message": "Password updated successfully"}
    raise response.error

@router.get("/user/history", response_model=list[AssignmentCompleteModel])
def get_user_history(month: int, user: Annotated[UserModel, Depends(SecurityController.get_current_user)]):
    """Get user history."""
    if not user:
        raise ResponseCode(status=401, message="User unauthorized").error
    controller = AssignmentController()
    response: Tuple[ResponseCode, list[dict]] = controller.get_user_assignments_completed_in_month(username=user.username, month=month)
    if response[0].status == 200:
        return response[1]
    raise response[0].error
