# app/config/schema.py

from pydantic import BaseModel
from typing import List

class EmployeeSchema(BaseModel):
    employee_id: int
    role: str
    work_experience: int

    class Config:
        schema_extra = {
            "example": {
                "employee_id": 501,
                "role": "Data Scientist",
                "work_experience": 5
            }
        }

class EmployeesListSchema(BaseModel):#Represents a response containing a list of employees.
    employees: List[EmployeeSchema]

    class Config:
        schema_extra = {
            "example": {
                "employees": [
                    {
                        "employee_id": 501,
                        "role": "Data Scientist",
                        "work_experience": 5
                    },
                    {
                        "employee_id": 502,
                        "role": "Software Engineer",
                        "work_experience": 3
                    }
                ]
            }
        }
