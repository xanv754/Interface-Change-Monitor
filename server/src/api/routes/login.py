from fastapi import APIRouter
from core import SecurityController, Settings
from errors import UNATHORIZED_USER
from schemas import Token, LoginParams

router = APIRouter()

@router.post("/login")
def login(data: LoginParams) -> Token:
    user = SecurityController.authenticate_user(data.username, data.password)
    if user is None:
        raise UNATHORIZED_USER
    settings = Settings()
    token = SecurityController.create_access_token(
        data={
            "sub": user.username,
            "profile": user.profile
        }
    )
    return Token(access_token=token, token_type=settings.TOKEN_TYPE_ACCESS)