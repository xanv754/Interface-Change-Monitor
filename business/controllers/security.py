import jwt
from typing import Annotated, Tuple
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from access.querys.user import UserQuery
from business.libs.code import ResponseCode
from business.models.token import TokenData
from business.models.user import UserModel
from utils.config import Configuration
from utils.log import log


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class SecurityController:
    _algorithm: str = "HS256"
    _key: str
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    access_token_expire_minutes: int = 540
    token_type_access: str = "bearer"

    def __init__(self):
        config = Configuration()
        self._key = config.key

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify the password of a user."""
        return self._pwd_context.verify(password, hashed_password)
    
    def _get_user(self, username: str) -> UserModel | None:
        """Get a user from the database."""
        try:
            query = UserQuery()
            user = query.get(username=username)
            if user is None: return None
            return user
        except Exception as error:
            log.error(f"Security access error. Failed to get user. {error}")
            return None
        
    def authenticate_user(self, username: str, password: str) -> UserModel | None:
        """Authenticate a user in the system.
        
        Parameters
        ----------
        username : str
            Username to authenticate.
        password : str
            Password to authenticate.
        """
        try:
            query = UserQuery()
            user = query.get(username=username)
            if user is None or not self._verify_password(password, user.password):
                return None
            return user
        except Exception as error:
            log.error(f"Security access error. Failed to authenticate user. {error}")
            return None
        
    def create_access_token(self, data: dict) -> str | None:
        """Create a token to access the system.
        
        Parameters
        ----------
        data : dict
            Data to create token.
        """
        try:
            to_encode = data.copy()
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.access_token_expire_minutes
            )
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(
                to_encode, self._key, algorithm=self._algorithm
            )
            return encoded_jwt
        except Exception as error:
            log.error(f"Security access error. Failed to create the access token. {error}")
            return None
        
    def create_password_hash(self, password: str) -> str:
        """Create a hash of the password of a user.
        
        Parameters
        ----------
        password : str
            Password to create hash.
        """
        return self._pwd_context.hash(password)
        
    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserModel | None:
        """Get the current user from the token.
        
        Parameters
        ----------
        token : Annotated[str, Depends(oauth2_scheme)]
            Token to get current user.
        """
        try:
            security = SecurityController()
            payload = jwt.decode(token, security._key, algorithms=[security._algorithm])
            username = payload.get("sub")
            if username is None: return None
            token = TokenData(username=username)
            user = security._get_user(username=username)
            if not user: None
            return user
        except Exception as error:
            log.error(f"Security access error. Failed to get current user. {error}")
            return None
