from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv
from os import getenv

load_dotenv(override=True)

URI = getenv("URI")
DATABASE = getenv("DATABASE")

def open_connection() -> Database:
    client = MongoClient(URI)
    db = client.get_database(DATABASE)
    return db

def close_connection():
    client = MongoClient(URI)
    client.close()