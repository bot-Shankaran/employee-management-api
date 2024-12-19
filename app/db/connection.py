# app/db/connection.py

from app.db.mongodb_config import get_database

def get_collection(collection_name: str):
    """
    Retrieve a MongoDB collection by name.
    
    Args:
        collection_name (str): The name of the collection to retrieve.
    
    Returns:
        Collection: The MongoDB collection instance.
    """
    db = get_database()
    return db[collection_name]
