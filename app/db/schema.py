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

class PaginatedEmployeesResponse(BaseModel):
    next_employee_id: Optional[int] = None
    employees: List[EmployeeSchema]

    class Config:
        schema_extra = {
            "example": {
                "next_employee_id": 510,
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
                    },
                    
                ]
            }
        }
}
