import jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from constants import ProfileType, AccountType
from core import SettingsSecurity
from controllers import OperatorController
from schemas import TokenData, OperatorSchema
from utils import encrypt, Log

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class SecurityCore:
    @staticmethod
    def create_access_token(data: dict) -> str:
        """Create a token to access the system.

        Parameters
        ----------
        data : dict
            Data to be encoded in the token.
        """
        settings = SettingsSecurity()
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def authenticate_user(username: str, password: str) -> OperatorSchema | None:
        """Authenticate a user in the system.

        Parameters
        ----------
        username : str
            Username of the user.
        password : str
            Password of the user.
        """
        user = OperatorController.get_operator(username, confidential=False)
        if user is None or not encrypt.verify_password(password, user.password):
            return None
        return user

    @staticmethod
    def get_access_root(
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> OperatorSchema | None:
        """Get the user with root privileges in the system.

        Parameters
        ----------
        token : Annotated[str, Depends(oauth2_scheme)]
            Token of the user.
        """
        try:
            user: OperatorSchema | None = SecurityCore.get_access_user(token)
            if not user:
                return None
            if user.account != AccountType.ACTIVE.value:
                return None
            if (
                user.profile == ProfileType.ROOT.value
                or user.profile == ProfileType.SOPORT.value
            ):
                return user
            return None
        except Exception as e:
            Log.save(e, __file__, Log.warning)
            return None

    @staticmethod
    def get_access_admin(
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> OperatorSchema | None:
        """Get the user with admin privileges in the system.

        Parameters
        ----------
        token : Annotated[str, Depends(oauth2_scheme)]
            Token of the user.
        """
        try:
            user: OperatorSchema | None = SecurityCore.get_access_user(token)
            if not user:
                return None
            if user.account != AccountType.ACTIVE.value:
                return None
            if (
                user.profile == ProfileType.ADMIN.value
                or user.profile == ProfileType.ROOT.value
                or user.profile == ProfileType.SOPORT.value
            ):
                return user
            return None
        except Exception as e:
            Log.save(e, __file__, Log.warning)
            return None

    @staticmethod
    def get_access_user(
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> OperatorSchema | None:
        """Get the user in the system.

        Parameters
        ----------
        token : Annotated[str, Depends(oauth2_scheme)]
            Token of the user.
        """
        try:
            settings = SettingsSecurity()
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                return None
            token_data = TokenData(username=username)
            user: OperatorSchema | None = OperatorController.get_operator(
                token_data.username
            )
            if user and user.account == AccountType.ACTIVE.value:
                return user
            else:
                return None
        except Exception as e:
            Log.save(e, __file__, Log.warning)
            return None
