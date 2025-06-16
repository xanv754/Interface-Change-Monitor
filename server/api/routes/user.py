from typing import Annotated, Tuple
from fastapi import APIRouter, Depends
from api.security.controller import SecurityController
from constants.code import ResponseCode
from controllers.user import UserController
from models.user import UserModel


router = APIRouter()


@router.get("/user")
def get_user():
    """Get user."""
    controller = UserController()
    response: Tuple[ResponseCode, UserModel | None] = controller.get_user(username="unittest")
    if response[0].status == 200:
        return response[1]
    raise response[0].error
