from fastapi import FastAPI
from app.api.controllers.crud_controller import router as employee_router
from app.utility.EnvConfig import MONGO_URI, DB_NAME
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
    print("\u2705 Connected to MongoDB")
    print(f"\ud83d\udd17 Mongo URI: {MONGO_URI}")
    print(f"\ud83d\uddcd Database: {DB_NAME}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True, log_level="debug")


# crud_controller.py
from fastapi import APIRouter, HTTPException, status, Query
from app.db.schema import EmployeeSchema, EmployeesListSchema, PaginatedEmployeesResponse
from app.dao.database_operation import (
    get_all_employees,
    get_employee_by_id,
    create_employee,
    update_employee,
    delete_employee
)
from typing import Optional

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

@router.get("/", response_model=EmployeesListSchema, summary="Retrieve All Employees")
def read_employees():
    """
    GET /employees
    Retrieve all employees.
    """
    employees = get_all_employees()
    return {"employees": employees}

@router.post("/", response_model=EmployeeSchema, status_code=status.HTTP_201_CREATED, summary="Create a New Employee")
def add_employee(employee: EmployeeSchema):
    """
    POST /employees
    Create a new employee.
    """
    existing_employee = get_employee_by_id(employee.employee_id)
    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with this ID already exists."
        )
    create_employee(employee)
    return employee

@router.put("/{employee_id}", response_model=dict, summary="Update an Existing Employee")
def modify_employee(employee_id: int, updates: dict):
    """
    PUT /employees/{employee_id}
    Update an existing employee by ID.
    """
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update."
        )
    success = update_employee(employee_id, updates)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found."
        )
    return {"message": "Employee updated successfully."}

@router.delete("/{employee_id}", response_model=dict, summary="Delete an Employee")
def remove_employee(employee_id: int):
    """
    DELETE /employees/{employee_id}
    Delete an employee by ID.
    """
    success = delete_employee(employee_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found."
        )
    return {"message": "Employee deleted successfully."}

@router.get("/cursor", response_model=PaginatedEmployeesResponse, summary="Retrieve Employees Using Cursor-Based Pagination")
def read_employees_cursor(
    last_employee_id: Optional[int] = Query(None, description="The last employee_id from the previous page"),
    page_size: int = Query(10, ge=1, le=100, description="Number of employees per page")
):
    """
    GET /employees/cursor
    Retrieve employees using cursor-based pagination.
    """
    employees = (
        employees_collection.find({"employee_id": {"$gt": last_employee_id}}) if last_employee_id
        else employees_collection.find()
    ).sort("employee_id", 1).limit(page_size)

    employees_list = [EmployeeSchema(**emp) for emp in employees]
    next_employee_id = employees_list[-1].employee_id if employees_list else None

    return {
        "next_employee_id": next_employee_id,
        "employees": employees_list
    }

