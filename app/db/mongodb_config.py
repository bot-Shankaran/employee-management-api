# app/config/mongodb_config.py

from pymongo import MongoClient
from app.Utility.EnvConfig import MONGO_URI, DB_NAME
def get_client():
    """
    Create a MongoDB client using the MONGO_URI from environment variables.
    """
    return MongoClient(MONGO_URI)

def get_database():
    """
    Get the MongoDB database using the DB_NAME from environment variables.
    """
    client = get_client()
    return client[DB_NAME]
