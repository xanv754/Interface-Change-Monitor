from dotenv import load_dotenv
from os import getenv
from utils.log import LogHandler


load_dotenv(override=True)


class SettingSecurityHandler:
    """Handler to get settings security of the system."""

    __instance: "SettingSecurityHandler | None" = None
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 59
    TOKEN_TYPE_ACCESS: str = "bearer"

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        try:
            if not hasattr(self, "__initialized"):
                secret_key = getenv("SECRET_KEY")
                if not secret_key:
                    raise ValueError("Variable 'SECRET_KEY' not found in environment file.")
                self.SECRET_KEY = secret_key
                self.__initialized = True
        except Exception as e:
            error = str(e)
            LogHandler(content=error, path=__file__, err=True)
            exit(1)
