import jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from core import Settings
from controllers import OperatorController
from schemas import TokenData, OperatorSchema
from utils import encrypt, Log

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class SecurityController:
    @staticmethod
    def create_access_token(data: dict) -> str:
        settings = Settings()
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> OperatorSchema | None:
        user = OperatorController.get_operator(username, confidential=False)
        if user is None or not encrypt.verify_password(password, user.password):
            return None
        return user
    
    @staticmethod
    async def get_access_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict | None:
        try:
            settings = Settings()
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("sub")
            if username is None: return None
            token_data = TokenData(username=username)
            user = OperatorController.get_operator(token_data.username)
            if user:
                return user.model_dump()
            else:
                return None
        except Exception as e:
            Log.save(e, __file__, Log.warning)
            return None

