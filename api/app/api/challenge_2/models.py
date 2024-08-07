from typing import Literal

from pydantic import BaseModel, Field

from app.core.constants import ReportType


class ReportTypeModel(BaseModel):
    """
    Model representing a report type.

    Attributes:
        report_type (ReportType): The type of the report.
    """

    report_type: ReportType = Field(...)
