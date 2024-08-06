from typing import Any, Dict, Optional

from pydantic import Field, BaseModel

from app.api.challenge_2.models import ReportTypeModel
from app.core.constants import NEW_TASK_SUCCESS_MESSAGE, TASK_TYPE
from app.api.challenge_1.models import UploadDataModel, TableNameModel


class ErrorModel(BaseModel):
    """
    Error Model for API responses.

    Attributes:
        status (Optional[str | int]): The status of the error response. Defaults to "error".
        message (str): The error message.
        error_type (str): The type of error.
        details (Optional[str | Dict[str, Any]]): Additional details about the error. Defaults to None.
    """

    status: Optional[str | int] = Field(default="error")
    message: str = Field(...)
    error_type: str = Field(...)
    details: Optional[str | Dict[str, Any]] = Field(None)

    class Config:
        extra = "ignore"
        json_schema_extra = {
            "example": {
                "status": "error",
                "message": "Error while processing request.",
                "error_type": "INVALID_TASK_CONFIGURATION",
                "details": {"detail": "detail"},
            }
        }


class KafkaTaskMessageModel(BaseModel):
    """
    Model representing a Kafka task message.

    Attributes:
        task_id (int): The ID of the task.
        task (TASK_TYPE): The type of the task.
        data (Optional[UploadDataModel]): Optional data associated with the task.
    """

    task_id: int = Field(...)
    task: TASK_TYPE = Field(...)
    data: Optional[UploadDataModel | TableNameModel | ReportTypeModel] = Field(None)


class TaskResponseModel(BaseModel):
    """
    Represents the response model for a task.

    Attributes:
        message (str): The message of the response.
        task_id (int): The ID of the task.
    """

    message: str = Field(...)
    task_id: int = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "message": NEW_TASK_SUCCESS_MESSAGE(1234, "<TASK_NAME>"),
                "task_id": 1234,
            }
        }
