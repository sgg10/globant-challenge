from typing import List, Optional

from pydantic import BaseModel, Field

from app.core.constants import NEW_TASK_SUCCESS_MESSAGE, TASK_TYPE


class DepartmentModel(BaseModel):
    """
    Represents a department model.

    Attributes:
        id (Optional[int]): The ID of the department.
        department (str): The name of the department.
    """

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
    """
    Represents a job model.

    Attributes:
        id (Optional[int]): The ID of the job model.
        job (str): The job title.
    """

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
    """
    Represents an employee.

    Attributes:
        id (Optional[int]): The ID of the employee.
        datetime (str): The date and time of the employee.
        name (str): The name of the employee.
        department_id (int): The ID of the department the employee belongs to.
        job_id (int): The ID of the job the employee has.
    """

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
    """
    Model representing uploaded data.

    Attributes:
        departments (List[DepartmentModel]): List of department models.
        jobs (List[JobModel]): List of job models.
        employees (List[EmployeeModel]): List of employee models.

    Properties:
        has_data (bool): Indicates if the model has any data.
        complies_data_size_limit (bool): Indicates if the model complies with the data size limit.
    """

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
