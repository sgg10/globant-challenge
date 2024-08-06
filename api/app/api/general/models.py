from typing import Optional
from pydantic import BaseModel, Field


class TaskResultModel(BaseModel):
    """
    Represents a task result.

    Attributes:
        id (int): The ID of the task result.
        name (str): The name of the task result.
        start_at (str): The start time of the task.
        end_at (str): The end time of the task.
        type (str): The type of the task.
        status (str): The status of the task.
        result (dict, optional): The result of the task (default: None).
    """

    id: int = Field(...)
    name: str = Field(...)
    type: str = Field(...)
    status: str = Field(...)
    start_at: Optional[str] = Field(None)
    end_at: Optional[str] = Field(None)
    result: Optional[dict] = Field(None)
