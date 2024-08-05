from typing import Any, Dict, Optional

from pydantic import Field, BaseModel


class ErrorModel(BaseModel):
    """Error Model for API responses."""

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
