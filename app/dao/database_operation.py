from app.db.connection import get_collection
from app.db.schema import EmployeeSchema
from typing import List, Optional

# Retrieve the 'employees' collection
employees_collection = get_collection("employees")

def get_all_employees() -> List[EmployeeSchema]:
    """
    Retrieve all employees from the database.
    
    Returns:
        List[EmployeeSchema]: A list of all employee records.
    """
    employees = employees_collection.find({}, {"_id": 0})
    return [EmployeeSchema(**emp) for emp in employees]

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

# Pagination with skip and limit
def get_employees_paginated(page: int = 1, page_size: int = 10) -> List[EmployeeSchema]:
    skip = (page - 1) * page_size
    employees = employees_collection.find({}, {"_id": 0}).skip(skip).limit(page_size)
    return [EmployeeSchema(**emp) for emp in employees]