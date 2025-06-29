from typing import Annotated
from datetime import timedelta
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from business.api.routes.changes import router as ChangesRouter
from business.api.routes.assignments import router as AssignmentsRouter
from business.api.routes.statistics import router as StatisticsRouter
from business.api.routes.history import router as HistoryRouter
from business.api.routes.user import router as UserRouter
from business.api.routes.configuration import router as ConfigurationRouter
from business.controllers.security import SecurityController
from business.libs.code import ResponseCode
from business.models.token import TokenModel


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(UserRouter)
app.include_router(AssignmentsRouter)
app.include_router(HistoryRouter)
app.include_router(StatisticsRouter)
app.include_router(ChangesRouter)
app.include_router(ConfigurationRouter)

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenModel:
    security = SecurityController()
    user = security.authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise ResponseCode(status=401, message="User incorrect").error
    access_token_expires = timedelta(minutes=security.access_token_expire_minutes)
    access_token = security.create_access_token(data={"sub": user.username})
    return TokenModel(access_token=access_token, token_type=security.token_type_access)