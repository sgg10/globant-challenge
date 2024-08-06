import os
from enum import Enum
from typing import Callable

from database.models import Department, Employee, Job

WORKERS = int(os.environ.get("WORKERS", 2))
AVAILABLE_CPU = max(os.cpu_count(), 1)
USE_CONCURRENCE = AVAILABLE_CPU >= 1

DB_HOST: str = os.getenv("DB_HOST", "localhost")
DB_PORT: str = os.getenv("DB_PORT", "5432")
DB_USER: str = os.getenv("DB_USER", "postgres")
DB_PASS: str = os.getenv("DB_PASSWORD", "postgres")
DB_NAME: str = os.getenv("DB_NAME", "mydb")

KAFKA_HOST: str = os.getenv("KAFKA_HOST", "kafka")
KAFKA_PORT: str = os.getenv("KAFKA_PORT", "29092")
KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "globant-challenge")
KAFKA_GROUP_ID: str = os.getenv("KAFKA_GROUP_ID", "globant-challenge-group")

DATABASE_CONNECTION_ERROR: str = "Error connecting to database"

CONSUMER_START_MESSAGE: str = "Starting consumer..."
CONSUMER_CLOSE_MESSAGE: str = "Closing consumer..."

PROCESS_TASK_INIT_MESSAGE: Callable[[int | str], str] = (
    lambda task_id: f"Processing task {task_id}..."
)
PROCESS_ALREADY_COMPLETED: Callable[[int | str], str] = (
    lambda task_id: f"Task {task_id} has already been completed."
)
PROCESS_ALREADY_FAILED: Callable[[int | str], str] = (
    lambda task_id: f"Task {task_id} has already failed."
)
PROCESS_TASK_SUCCESS: Callable[[int | str], str] = (
    lambda task_id: f"Task {task_id} has been successfully processed."
)
PROCESS_TASK_FAILED: Callable[[int | str], str] = (
    lambda task_id: f"Task {task_id} has failed."
)


class TaskTypeIdEnum(int, Enum):
    LOAD = 1
    BACKUP = 2
    RESTORE = 3
    REPORT = 4
    MIGRATION = 5


class TaskStatusIdEnum(int, Enum):
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    FAILED = 4


BASE_CHALLENGE_1_CONFIG_MAP = {
    "department": {
        "model": Department,
    },
    "job": {
        "model": Job,
    },
    "employee": {
        "model": Employee,
    },
}

LOAD_CHALLENGE_1_CONFIG_MAP = {
    f"{k}s": v for k, v in BASE_CHALLENGE_1_CONFIG_MAP.items()
}

LOAD_DUPLICATE_KEY_VALUE_ERROR: str = "duplicate key value violates unique constraint"
LOAD_CANNOT_INSERT_DUPLICATE: str = "Cannot insert duplicate data"
LOAD_INVALID_ROW: Callable[[dict], str] = (
    lambda row: f"Invalid row {row}: missing required fields"
)
LOAD_INVALID_ROWS_FOUND: Callable[[str], str] = (
    lambda model_name: f"Invalid rows found in {model_name}"
)
LOAD_DATA_SUCCESS: str = "Data loaded successfully"

BACKUP_SUCCESS: Callable[[str], str] = (
    lambda table_name: f"Backup for {table_name} successful"
)
BACKUP_FAILED: Callable[[str], str] = (
    lambda table_name: f"Backup for {table_name} failed"
)

RESTORE_NOT_FOUND_IN_S3: str = "Restore failed: data not found in S3"
RESTORE_SUCCESS: Callable[[str], str] = (
    lambda table_name: f"Restore for {table_name} successful"
)

S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "sgg-globant-challenge")
S3_BACKUP_PATH: str = "backups"


REPORT_TYPE1_TEMPLATE: str = "type1.md"
REPORT_TYPE1_NAME: str = "Quarterly Hiring Report by Job and Department for 2021"
REPORT_TYPE1_OUTPUT: str = "quarterly_hiring_report_2021"

REPORT_TYPE2_TEMPLATE: str = "type2.md"
REPORT_TYPE2_NAME: str = "Departments Hiring Above Mean in 2021"
REPORT_TYPE2_OUTPUT: str = "departments_hiring_above_mean_2021"
REPORT_FAIL_S3_UPLOAD: str = "Failed to upload report to S3"
REPORT_FAIL_URL_GENERATION: str = "Failed to generate pre-signed URL"
REPORT_GENERATED_SUCCESS: str = "Report generated and uploaded successfully"
