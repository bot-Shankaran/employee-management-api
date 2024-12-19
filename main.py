from fastapi import FastAPI
from app.api.Controller.crud_controller import router as employee_router
from app.Utility.EnvConfig import MONGO_URI, DB_NAME
import uvicorn

app = FastAPI(
    title="Employee Management API",
    description="API for managing employees in the company database.",
    version="1.0.0"
)

# Include the Employee Router
app.include_router(employee_router)

@app.get("/", summary="Root Endpoint")
def root():
    """
    GET /
    Welcome message for the Employee API.
    """
    return {"message": "Welcome to the Employee API!"}

@app.get("/usage", summary="API Usage Instructions")
def usage():
    """
    GET /usage
    Provides information on how to use the CRUD endpoints.
    """
    return {
        "GET": {
            "description": "Retrieve all employees",
            "endpoint": "/employees",
            "method": "GET"
        },
        "POST": {
            "description": "Create a new employee",
            "endpoint": "/employees",
            "method": "POST",
            "example_payload": {
                "employee_id": 501,
                "role": "Data Scientist",
                "work_experience": 5
            }
        },
        "PUT": {
            "description": "Update an existing employee by ID",
            "endpoint": "/employees/{employee_id}",
            "method": "PUT",
            "example_payload": {
                "work_experience": 10
            }
        },
        "DELETE": {
            "description": "Delete an employee by ID",
            "endpoint": "/employees/{employee_id}",
            "method": "DELETE"
        }
    }

@app.on_event("startup")
async def startup_event():
    """
    Event handler that runs on application startup.
    """
    print("✅ Connected to MongoDB")
    print(f"🔗 Mongo URI: {MONGO_URI}")
    print(f"📂 Database: {DB_NAME}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True, log_level="debug")
