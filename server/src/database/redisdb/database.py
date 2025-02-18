import redis
from os import getenv
from dotenv import load_dotenv

load_dotenv()   

URI = getenv('URI_REDIS')

class RedisDatabase:
    _instance: "RedisDatabase | None" = None
    connection: redis.Redis

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, "_initialized"):
            self.connection = redis.Redis.from_url(URI)
            self._initialized = True

    def get_connection(self) -> redis.Redis:
        return self.connection
    
    def close_connection(self) -> None:
        self.connection.close()