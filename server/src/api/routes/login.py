from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api import error
from core import SecurityCore, SettingsSecurity
from schemas import TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenResponse:
    """Login to the system.

    **Request params:**
    - username: Username of the user
    - password: Password of the user
    """
    user = SecurityCore.authenticate_user(data.username, data.password)
    if user is None:
        raise error.UNATHORIZED_USER
    settings = SettingsSecurity()
    token = SecurityCore.create_access_token(data={"sub": user.username})
    return TokenResponse(accessToken=token, typeToken=settings.TOKEN_TYPE_ACCESS)
