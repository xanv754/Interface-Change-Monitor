from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api import LoginRouter, OperatorRouter
from api import LOGIN_PREFIX, OPERATOR_PREFIX
from api import UNATHORIZED_USER
from core import SecurityCore, Settings
from schemas import Token

app = FastAPI()

app.include_router(LoginRouter, prefix=f"/api/{LOGIN_PREFIX}")
app.include_router(OperatorRouter, prefix=f"/api/{OPERATOR_PREFIX}")

@app.post("/token", response_model=Token)
async def login(data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = SecurityCore.authenticate_user(data.username, data.password)
    if user is None:
        raise UNATHORIZED_USER
    settings = Settings()
    token = SecurityCore.create_access_token(
        data={"sub": user.username}
    )
    return Token(access_token=token, token_type=settings.TOKEN_TYPE_ACCESS)