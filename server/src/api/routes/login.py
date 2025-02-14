from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api import error
from core import SecurityCore, Settings
from schemas import Token

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """Login to the system.

    **Request body:**
    - username: Username of the user
    - password: Password of the user
    """
    user = SecurityCore.authenticate_user(data.username, data.password)
    if user is None:
        raise error.UNATHORIZED_USER
    settings = Settings()
    token = SecurityCore.create_access_token(
        data={"sub": user.username}
    )
    return Token(access_token=token, token_type=settings.TOKEN_TYPE_ACCESS)