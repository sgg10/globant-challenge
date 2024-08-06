import json
from fastapi import Path, status, APIRouter, HTTPException

from app.core import constants
from app.api.models import ErrorModel
from app.database.connection import create_session
from app.api.general.models import TaskResultModel
from app.database.models import Task, TaskStatus, TaskType

from app.kafka.check_health import check_kafka_health
from app.database.check_health import check_database_health

router = APIRouter(prefix="", tags=[])


@router.get("/health")
def health():
    """
    # Health

    Endpoint for checking the health status of the API.

    ## Returns:
        dict: A dictionary containing the health status of the database, Kafka, and the general status of the API.
    """
    database_health, database_message = check_database_health()
    kafka_health, kafka_message = check_kafka_health()
    return {
        "database": {
            "status": "ok" if database_health else "error",
            "message": database_message,
        },
        "kafka": {
            "status": "ok" if kafka_health else "error",
            "message": kafka_message,
        },
        "general_status": "ok" if all([database_health, kafka_health]) else "error",
    }


@router.get(
    path=constants.GENERAL_TASKS_ENDPOINT,
    status_code=status.HTTP_200_OK,
    summary=constants.GENERAL_TASKS_ENDPOINT_SUMMARY,
    response_model=TaskResultModel,
)
def get_task(task_id: int = Path(...)):
    """
    # Get Task Information

    Get information about a specific task based on the task ID.

    ## Parameters:
        task_id (int): The ID of the task.

    ## Returns:
        dict: The task information.
    """
    try:
        _, session = create_session()

        task = (
            session.query(
                Task.id.label("id"),
                Task.name.label("name"),
                Task.config.label("config"),
                Task.start_at.label("start_at"),
                Task.end_at.label("end_at"),
                TaskType.name.label("type"),
                TaskStatus.name.label("status"),
            )
            .join(TaskType, Task.type_id == TaskType.id)
            .join(TaskStatus, Task.status_id == TaskStatus.id)
            .filter(Task.id == task_id)
            .first()
        )

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorModel(
                    code=status.HTTP_404_NOT_FOUND,
                    message=constants.ResponseErrorMessage.TASK_NOT_FOUND,
                    error_type=constants.ResponseErrorTypeEnum.TASK_NOT_FOUND,
                    details=constants.ResponseErrorMessage.TASK_NOT_FOUND,
                ).model_dump(),
            )

        task_info = {
            "id": task.id,
            "name": task.name,
            "config": task.config,
            "start_at": task.start_at,
            "end_at": task.end_at,
            "type": task.type,
            "status": task.status,
        }

        session.close()

        task_info["start_at"] = (
            task_info["start_at"].strftime("%Y-%m-%d %H:%M:%S")
            if task_info["start_at"]
            else None
        )
        task_info["end_at"] = (
            task_info["end_at"].strftime("%Y-%m-%d %H:%M:%S")
            if task_info["end_at"]
            else None
        )

        if task_info["status"] == constants.TaskStatusEnum.COMPLETED:
            task_info["result"] = json.loads(task_info["config"]).get("result", None)

        del task_info["config"]

        return TaskResultModel(**task_info)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorModel(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=constants.ResponseErrorMessage.HTTP_500,
                error_type=constants.ResponseErrorTypeEnum.HTTP_500,
                details=str(e),
            ).model_dump(),
        )
