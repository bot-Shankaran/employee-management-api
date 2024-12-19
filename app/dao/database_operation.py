from app.db.connection import get_collection
from app.db.schema import EmployeeSchema
from typing import List, Optional

# Retrieve the 'employees' collection
employees_collection = get_collection("employees")

def get_all_employees(skip: int, limit: int) -> List[EmployeeSchema]:
    """
    Retrieve all employees from the database with pagination.
    
    Args:
        skip (int): Number of records to skip.
        limit (int): Number of records to fetch.
    
    Returns:
        List[EmployeeSchema]: A paginated list of employee records.
    """
    employees = employees_collection.find({}, {"_id": 0}).skip(skip).limit(limit)
    return [EmployeeSchema(**emp) for emp in employees]

def create_multiple_employees(employees: List[EmployeeSchema]) -> dict:
    """
    Insert multiple employees into the database.
    
    Args:
        employees (List[EmployeeSchema]): List of employee data to insert.
    
    Returns:
        dict: Information about the insert operation.
    """
    result = employees_collection.insert_many([employee.dict() for employee in employees])
    return {"inserted": len(result.inserted_ids)}

def get_employee_by_id(employee_id: int) -> Optional[EmployeeSchema]:
    """
    Retrieve a single employee by employee_id.
    
    Args:
        employee_id (int): The ID of the employee to retrieve.
    
    Returns:
        Optional[EmployeeSchema]: The employee record if found, else None.
    """
    employee = employees_collection.find_one({"employee_id": employee_id}, {"_id": 0})
    if employee:
        return EmployeeSchema(**employee)
    return None

def create_employee(employee: EmployeeSchema) -> EmployeeSchema:
    """
    Insert a new employee into the database.
    
    Args:
        employee (EmployeeSchema): The employee data to insert.
    
    Returns:
        EmployeeSchema: The inserted employee data.
    """
    employees_collection.insert_one(employee.dict())
    return employee

def update_employee(employee_id: int, updates: dict) -> bool:
    """
    Update an existing employee's details.
    
    Args:
        employee_id (int): The ID of the employee to update.
        updates (dict): A dictionary of fields to update.
    
    Returns:
        bool: True if the update was successful, False otherwise.
    """
    result = employees_collection.update_one({"employee_id": employee_id}, {"$set": updates})
    return result.matched_count > 0

def delete_employee(employee_id: int) -> bool:
    """
    Delete an employee from the database.
    
    Args:
        employee_id (int): The ID of the employee to delete.
    
    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    result = employees_collection.delete_one({"employee_id": employee_id})
    return result.deleted_count > 0
