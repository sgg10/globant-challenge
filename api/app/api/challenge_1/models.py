from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError


class DepartmentModel(BaseModel):
    id: Optional[int] = Field(None)
    department: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1234,
                "department": "HR",
            }
        }


class JobModel(BaseModel):
    id: Optional[int] = Field(None)
    job: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1234,
                "job": "Manager",
            }
        }


class EmployeeModel(BaseModel):
    id: Optional[int] = Field(None)
    datetime: str = Field(..., format="date-time")
    name: str = Field(
        ...,
    )
    department_id: int = Field(...)
    job_id: int = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1234,
                "datetime": "2021-09-01T00:00:00",
                "name": "John Doe",
                "department_id": 1234,
                "job_id": 1234,
            }
        }


class UploadDataModel(BaseModel):
    departments: List[DepartmentModel] = Field(default_factory=list)
    jobs: List[JobModel] = Field(default_factory=list)
    employees: List[EmployeeModel] = Field(default_factory=list)

    @property
    def has_data(self):
        return bool(self.departments or self.jobs or self.employees)

    @property
    def complies_data_size_limit(self):
        return len(self.departments) + len(self.jobs) + len(self.employees) <= 1000

    class Config:
        json_schema_extra = {
            "example": {
                "departments": [
                    {
                        "id": 1234,
                        "department": "HR",
                    }
                ],
                "jobs": [
                    {
                        "id": 1234,
                        "job": "Manager",
                    }
                ],
                "employees": [
                    {
                        "id": 1234,
                        "datetime": "2021-09-01T00:00:00",
                        "name": "John Doe",
                        "department_id": 1234,
                        "job_id": 1234,
                    }
                ],
            }
        }
