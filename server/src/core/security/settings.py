from dotenv import load_dotenv
from os import getenv
from utils import Log

load_dotenv()


class SettingsSecurity:
    """Settings basic of the security of the system."""

    _instance: "SettingsSecurity | None" = None
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 59
    TOKEN_TYPE_ACCESS: str = "bearer"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        try:
            if not hasattr(self, "_initialized"):
                self.SECRET_KEY = getenv("SECRET_KEY")
                self._initialized = True
        except Exception as e:
            Log.save(e, __file__, Log.error)
