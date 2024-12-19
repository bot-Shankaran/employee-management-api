from fastapi import APIRouter, HTTPException, status, Query
from app.db.schema import EmployeeSchema, EmployeesListSchema
from app.dao.database_operation import (
    get_all_employees,
    get_employee_by_id,
    create_employee,
    create_multiple_employees,
    update_employee,
    delete_employee
)
import logging

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)

@router.get("/", response_model=EmployeesListSchema, summary="Retrieve All Employees")
def read_employees(skip: int = Query(0, ge=0), limit: int = Query(10, gt=0)):
    """
    GET /employees
    Retrieve all employees with pagination.
    """
    logger.info("Fetching employees with pagination - Skip: %d, Limit: %d", skip, limit)
    employees = get_all_employees(skip, limit)
    return {"employees": employees}

@router.post("/", response_model=EmployeeSchema, status_code=status.HTTP_201_CREATED, summary="Create a New Employee")
def add_employee(employee: EmployeeSchema):
    """
    POST /employees
    Create a new employee.
    """
    logger.info("Creating a new employee with ID: %d", employee.employee_id)
    existing_employee = get_employee_by_id(employee.employee_id)
    if existing_employee:
        logger.warning("Employee with ID %d already exists.", employee.employee_id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with this ID already exists."
        )
    create_employee(employee)
    logger.info("Employee with ID %d created successfully.", employee.employee_id)
    return employee

@router.post("/bulk", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Add Multiple Employees")
def add_employees_bulk(employees: EmployeesListSchema):
    """
    POST /employees/bulk
    Add multiple employees.
    """
    logger.info("Adding multiple employees.")
    result = create_multiple_employees(employees.employees)
    logger.info("Bulk insert completed. Total inserted: %d", result["inserted"])
    return {"message": "Employees added successfully.", "inserted": result["inserted"]}



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
