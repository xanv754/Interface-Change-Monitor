from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from modules.security import login_for_access_token
from models.register import RegisterModel
from modules.manager import Manager
from typing import Annotated

router = APIRouter()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password", 
    headers={"WWW-Authenticate": "Bearer"},
)

@router.post("/api/v1/register", status_code=status.HTTP_201_CREATED)
def create_new_user(data: RegisterModel):
    res = Manager.create_new_user(data)
    if res and res == 0: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not created")
    elif res and res == 2: raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Existing user")
    elif res and res == 1: return {"created": "1"}
    else: raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown error")

@router.post("/api/v1/login")
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):    
    token = login_for_access_token(form_data)
    if not token: raise credentials_exception
    return token

@router.put("/api/v1/login/username={username}/newPassword={new_password}", status_code=status.HTTP_204_NO_CONTENT)
def forgot_password(username: str, new_password: str):
    res = Manager.forgot_password(username, new_password)
    if not res: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else: return
    