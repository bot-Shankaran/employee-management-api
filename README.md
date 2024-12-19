# Directory Structure
project-root/
│ 
├── app/ 
│   │ 
│   ├── api/ 
│   │   ├── __init__.py 
│   │   └── controllers/ 
│   │       ├── __init__.py 
│   │       └── crud_controller.py 
│   │
│   │
│   ├── dao/
│   │   ├── __init__.py
│   │   └── database_operation.py
│   │ 
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   └── connection.py
│   │   ├── mongodb_config.py 
│   │   └── schema.py
│   │
│   │
│   │
│   └── utility/
│       ├── __init__.py
│       ├── development.env 
│       └── EnvConfig.py 
├── main.py
├── .gitignore 
├── README.md 
└── requirements.txt 



# Prerequisites
Before you begin, ensure you have met the following requirements:

Python 3.8 or higher
MongoDB: Download MongoDB
Git: Download Git



# Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.
# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate


# Install Dependencies
With the virtual environment activated, install the required packages:

pip install -r requirements.txt



# Prerequisites
Before you begin, ensure you have met the following requirements:

Python 3.8 or higher: Download Python
MongoDB: Download MongoDB
Git: Download Git


# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate


# Install Dependencies
With the virtual environment activated, install the required packages:

pip install -r requirements.txt


# Configuration
 Environment Variables
The application uses environment variables for configuration. These are stored in the development.env file.
app/utility/development.env

# database info
MONGO_URI=mongodb://localhost:27017/
DB_NAME=company_db
MONGO_URI: The connection string for your MongoDB instance.
DB_NAME: The name of the MongoDB database to use.
Ensure MongoDB is running and accessible at the specified MONGO_URI.

Loading Environment Variables
The EnvConfig.py module loads these variables:
app/utility/EnvConfig.py

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




# Running the Application
uvicorn main:app --reload
Swagger UI: http://127.0.0.1:5000/docs
