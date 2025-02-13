from fastapi import FastAPI
from api import LoginRouter
from constants import LOGIN_PREFIX

app = FastAPI()

app.include_router(LoginRouter, prefix=f"/api/{LOGIN_PREFIX}")

@app.get("/")
def read_root():
    return {"Hello": "World"}