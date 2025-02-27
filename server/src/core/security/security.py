import jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from constants import ProfileType, AccountType
from core import SettingsSecurity
from controllers.operator import OperatorController
from schemas import TokenData, OperatorResponseSchema
from utils import encrypt, Log

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class SecurityCore:
    @staticmethod
    def create_access_token(data: dict, token_expire: bool = False) -> str | None:
        """Create a token to access the system.

        Parameters
        ----------
        data : dict
            Data to be encoded in the token.
        """
        try:
            settings = SettingsSecurity()
            to_encode = data.copy()
            if token_expire:
                expire = datetime.now(timezone.utc) + timedelta(
                    minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
                )
                to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(
                to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
            )
            return encoded_jwt
        except Exception as e:
            Log.save(f"Failed to create the access token. {e}", __file__, Log.error, console=True)
            return None

    @staticmethod
    def authenticate_user(username: str, password: str) -> OperatorResponseSchema | None:
        """Authenticate a user in the system.

        Parameters
        ----------
        username : str
            Username of the user.
        password : str
            Password of the user.
        """
        try:
            user = OperatorController.get_operator(username, confidential=False)
            if user is None or not encrypt.verify_password(password, user.password):
                raise Exception("User incorrect. Don't have access to the system")
            return user
        except Exception as e:
            Log.save(e, __file__, Log.warning)
            return None

    @staticmethod
    def get_access_root(
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> OperatorResponseSchema | None:
        """Get the user with root privileges in the system.

        Parameters
        ----------
        token : Annotated[str, Depends(oauth2_scheme)]
            Token of the user.
        """
        try:
            user: OperatorResponseSchema | None = SecurityCore.get_access_user(token)
            if not user:
                raise Exception("User not found. Don't have access to the system")
            if user.account != AccountType.ACTIVE.value:
                raise Exception("User not active. Don't have access to the system")
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
    ) -> OperatorResponseSchema | None:
        """Get the user with admin privileges in the system.

        Parameters
        ----------
        token : Annotated[str, Depends(oauth2_scheme)]
            Token of the user.
        """
        try:
            user: OperatorResponseSchema | None = SecurityCore.get_access_user(token)
            if not user:
                raise Exception("User not found. Don't have access to the system")
            if user.account != AccountType.ACTIVE.value:
                raise Exception("User not active. Don't have access to the system")
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
    ) -> OperatorResponseSchema | None:
        """Get the user in the system.

        Parameters
        ----------
        token : Annotated[str, Depends(oauth2_scheme)]
            Token of the user.
        """
        try:
            settings = SettingsSecurity()
            if not token:
                raise Exception("Token not obtained. Don't have access to the system")
            payload = jwt.decode(
                jwt=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise Exception("Username not obtained. Don't have access to the system")
            token_data = TokenData(username=username)
            user: OperatorResponseSchema | None = OperatorController.get_operator(
                token_data.username
            )
            if user and user.account == AccountType.ACTIVE.value:
                return user
            else:
                raise Exception("User not found or not active. Don't have access to the system")
        except Exception as e:
            Log.save(e, __file__, Log.warning)
            return None
