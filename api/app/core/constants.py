import os
from enum import Enum
from typing import Callable, Literal


# Constants

API_PREFIX: str = os.getenv("API_PREFIX", "")
API_NAME: str = os.getenv("API_NAME", "Globant-Challaenge-API")
API_VERSION: str = os.getenv("VERSION", "v0.1.0")
API_ORIGINS: str = os.getenv("ORIGINS", "*")
API_ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")

DB_HOST: str = os.getenv("DB_HOST", "db")
DB_PORT: str = os.getenv("DB_PORT", "5432")
DB_USER: str = os.getenv("DB_USER", "postgres")
DB_PASS: str = os.getenv("DB_PASSWORD", "postgres")
DB_NAME: str = os.getenv("DB_NAME", "mydb")

KAFKA_HOST: str = os.getenv("KAFKA_HOST", "kafka")
KAFKA_PORT: str = os.getenv("KAFKA_PORT", "29092")
KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "globant-challenge")

DATABASE_CHECK_HEALTH_QUERY: str = "SELECT 1"
KAFKA_CHECK_HEALTH_SUCCESS: str = f"Topic '{KAFKA_TOPIC}' exists."

CHALLENGE_1_PREFIX: str = "challenge-1"

CHALLENGE_1_UPLOAD_ENDPOINT: str = ""
CHALLENGE_1_UPLOAD_ENDPOINT_SUMMARY: str = (
    "Upload data for departments, jobs, or employees"
)

CHALLENGE_1_BACKUP_ENDPOINT: str = "/backup"
CHALLENGE_1_BACKUP_ENDPOINT_SUMMARY: str = (
    "Backup data for departments, jobs, or employees"
)

CHALLENGE_1_RESTORE_ENDPOINT: str = "/restore"
CHALLENGE_1_RESTORE_ENDPOINT_SUMMARY: str = (
    "Restore data for departments, jobs, or employees"
)

NEW_TASK_SUCCESS_MESSAGE: Callable[[int, str], str] = (
    lambda id, name: f"'{name}' task created with id '{id}'. Use this id to check the task status"
)

CHALLENGE_2_PREFIX: str = "challenge-2"
CHALLENGE_2_REPORT_ENDPOINT: str = "/report/{type}"
CHALLENGE_2_REPORT_ENDPOINT_SUMMARY: str = "Request a report from the database"


# Enums and Types


class TaskTypeEnum(str, Enum):
    LOAD = "LOAD"
    BACKUP = "BACKUP"
    RESTORE = "RESTORE"
    REPORT = "REPORT"


TASK_TYPE = Literal[
    TaskTypeEnum.LOAD, TaskTypeEnum.BACKUP, TaskTypeEnum.RESTORE, TaskTypeEnum.REPORT
]


class TaskStatusEnum(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ReportTypeEnum(str, Enum):
    TYPE1 = "type1"
    TYPE2 = "type2"


ReportType = Literal[ReportTypeEnum.TYPE1, ReportTypeEnum.TYPE2]


class TableEnum(str, Enum):
    DEPARTMENT = "department"
    JOB = "job"
    EMPLOYEE = "employee"


TableType = Literal[TableEnum.DEPARTMENT, TableEnum.JOB, TableEnum.EMPLOYEE]


class ResponseErrorTypeEnum(str, Enum):
    HTTP_500: str = "INTERNAL_SERVER_ERROR"
    NO_DATA_PROVIDED: str = "NO_DATA_PROVIDED"
    DATA_SIZE_LIMIT_EXCEEDED: str = "DATA_SIZE_LIMIT_EXCEEDED"
    REPORT_NOT_FOUND: str = "REPORT_NOT_FOUND"


class ResponseErrorMessage(str, Enum):
    HTTP_500: str = "Internal Server Error"
    NO_DATA_PROVIDED: str = "No data provided"
    DATA_SIZE_LIMIT_EXCEEDED: str = "The data size limit is 1000 records per request"
    REPORT_NOT_FOUND: str = "The specified report does not exist"


# Error messages
KAFKA_CHECK_HEALTH_ERROR: str = "Error checking Kafka health"
KAFKA_CHECK_HEALTH_NO_EXISTS_TOPIC_ERROR: str = (
    f"{KAFKA_CHECK_HEALTH_ERROR}: Topic '{KAFKA_TOPIC}' does not exist."
)

DATABASE_CHECK_HEALTH_ERROR: str = "Error checking database health"
DATABASE_CONNECTION_ERROR: str = "Error connecting to database"
