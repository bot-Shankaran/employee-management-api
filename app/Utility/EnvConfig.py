# app/utility/EnvConfig.py

import os
from dotenv import load_dotenv

# Define the path to the .env file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, "development.env")

# Load environment variables from the .env file
load_dotenv(dotenv_path=env_path)

# Retrieve environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "company_db")
