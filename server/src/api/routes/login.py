from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api import error
from controllers import SecurityController, SettingsSecurityHandler
from schemas import TokenResponseSchema

router = APIRouter()


@router.post("/login", response_model=TokenResponseSchema)
async def login(data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenResponseSchema:
    """Login to the system.

    **Request params:**
    - username: Username of the user
    - password: Password of the user
    """
    user = SecurityController.authenticate_user(data.username, data.password)
    if user is None:
        raise error.UNATHORIZED_USER
    settings = SettingsSecurityHandler()
    token = SecurityController.create_access_token(data={"sub": user.username})
    return TokenResponseSchema(access_token=token, token_type=settings.TOKEN_TYPE_ACCESS)
