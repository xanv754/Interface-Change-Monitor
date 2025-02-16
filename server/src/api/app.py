from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api import (
    prefix,
    error,
    LoginRouter,
    OperatorRouter,
    AdministrationRouter,
    StatisticsRouter,
    HistoryRouter,
    ConfigRouter
)
from core import SecurityCore, SettingsSecurity
from schemas import Token

app = FastAPI()

app.include_router(LoginRouter, prefix=f"/api/{prefix.LOGIN}")
app.include_router(OperatorRouter, prefix=f"/api/{prefix.OPERATOR}")
app.include_router(AdministrationRouter, prefix=f"/api/{prefix.ADMINISTRATION}")
app.include_router(StatisticsRouter, prefix=f"/api/{prefix.STATISTICS}")
app.include_router(HistoryRouter, prefix=f"/api/{prefix.HISTORY}")
app.include_router(ConfigRouter, prefix=f"/api/{prefix.CONFIG}")


@app.post("/token", response_model=Token)
async def login(data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """Login to the system for swagger.

    **Request params:**
    - username: Username of the user
    - password: Password of the user
    """
    user = SecurityCore.authenticate_user(data.username, data.password)
    if user is None:
        raise error.UNATHORIZED_USER
    settings = SettingsSecurity()
    token = SecurityCore.create_access_token(data={"sub": user.username})
    return Token(access_token=token, token_type=settings.TOKEN_TYPE_ACCESS)
