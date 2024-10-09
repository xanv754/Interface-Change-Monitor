from fastapi.middleware.cors import CORSMiddleware
from route.elements import router as element_router
from route.login import router as login_router
from route.user import router as user_router
from dotenv import load_dotenv
from fastapi import FastAPI
from os import getenv

load_dotenv()
app = FastAPI()

URL_PAGE = getenv("URL_PAGE")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router)
app.include_router(element_router)
app.include_router(user_router)