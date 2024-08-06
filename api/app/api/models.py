from typing import Any, Dict, Optional

from pydantic import Field, BaseModel


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
