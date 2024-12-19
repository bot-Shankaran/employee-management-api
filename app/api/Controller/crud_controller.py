from fastapi import APIRouter, HTTPException, status
from app.db.schema import EmployeeSchema
from app.dao.database_operation import (
    get_all_employees,
    get_employee_by_id,
    create_employee,
    update_employee,
    delete_employee
)
from typing import Optional
from app.db.schema import PaginatedEmployeesResponse



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
def read_employees_cursor(last_employee_id: Optional[int] = Query(None, description="The last employee_id from the previous page"),
                          page_size: int = Query(10, ge=1, le=100, description="Number of employees per page")):
    """
    GET /employees/cursor
    Retrieve employees using cursor-based pagination.
    
    Args:
        last_employee_id (int, optional): The employee_id after which to fetch employees.
        page_size (int): Number of employees to fetch.
    
    Returns:
        PaginatedEmployeesResponse: A response containing the next_employee_id and a list of employees.
    """
    if last_employee_id is None:
        # Fetch the first page
        employees = employees_collection.find({}, {"_id": 0}).sort("employee_id", 1).limit(page_size)
    else:
        # Fetch employees after the last_employee_id
        employees = employees_collection.find(
            {"employee_id": {"$gt": last_employee_id}},
            {"_id": 0}
        ).sort("employee_id", 1).limit(page_size)
    
    employees_list = [EmployeeSchema(**emp) for emp in employees]
    if employees_list:
        next_employee_id = employees_list[-1].employee_id
    else:
        next_employee_id = None
    
    return {
        "next_employee_id": next_employee_id,
        "employees": employees_list
    }