from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, Depends, status
from controllers.admin import AdminController
from jwt.exceptions import InvalidTokenError
from constants.userStatus import userstatus
from passlib.context import CryptContext
from models.access import AccessModel
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends
from os import getenv
import jwt

load_dotenv(override=True)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = getenv("JWT_ALGORITHM")
JWT_TOKEN_EXPIRE = int(getenv("JWT_TOKEN_EXPIRE"))

def secure_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token(data: dict, expires_delta: (timedelta | None)) -> str:
    to_encode = data.copy()
    if expires_delta: expire = datetime.now(timezone.utc) + expires_delta
    else: expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: Annotated[str, Depends(oauth2_scheme)]) -> (str | None):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        username: str = payload.get("sub")
        if not username: return None
        else: return username
    except InvalidTokenError:
        return None
    
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> (dict | None):
    try:
        username = verify_token(token)
        if not username: return None
        user = AdminController.search_user(username)
        if not user: return None
        if user.status != userstatus.enabled: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not accessible")
        else: 
            user = user.model_dump(exclude={'password', 'lastPassword'})
            return user
    except Exception as error:
        print(error)
        raise None
        
def authenticate_user(username: str, password: str):
    user = AdminController.search_user(username)
    if user:
        if verify_password(password, user.password): return user
    return None

def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> (AccessModel | None):
    user = authenticate_user(form_data.username, form_data.password)
    if not user or user.status != userstatus.enabled: return None
    access_token_expires = timedelta(minutes=JWT_TOKEN_EXPIRE)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return AccessModel(access_token=access_token, token_type="bearer")