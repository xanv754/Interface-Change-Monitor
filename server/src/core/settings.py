from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Settings:
    _instance: "Settings | None" = None
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 59
    TOKEN_TYPE_ACCESS: str = "bearer"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.SECRET_KEY = getenv("SECRET_KEY")
            self._initialized = True