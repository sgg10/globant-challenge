from uuid import uuid4
from typing import Optional

from fastapi import status, HTTPException

from app.api.models import ErrorModel
from app.core.settings import APISettings
from app.kafka.producer import get_kafka_producer
from app.database.connection import create_session
from app.core.constants import (
    DATABASE_CONNECTION_ERROR,
    NEW_TASK_SUCCESS_MESSAGE,
    TASK_TYPE,
    TaskStatusEnum,
    ResponseErrorMessage,
    ResponseErrorTypeEnum,
)
from app.database.models import (
    Task,
    TaskType,
    TaskStatus,
)
from app.api.challenge_1.models import (
    UploadDataModel,
    KafkaTaskMessageModel,
    TaskResponseModel,
)


def create_task(task_type: TASK_TYPE):
    try:
        engine, session = create_session()

        if not engine or not session:
            return None, DATABASE_CONNECTION_ERROR

        pending_id = (
            session.query(TaskStatus).filter_by(name=TaskStatusEnum.PENDING).first().id
        )
        upload_id = session.query(TaskType).filter_by(name=task_type).first().id

        task = Task(
            name=f"{task_type}-{uuid4()}", type_id=upload_id, status_id=pending_id
        )

        session.add(task)
        session.commit()

        task_info = {
            "id": task.id,
            "name": task.name,
        }

        session.close()

        return task_info, None
    except Exception as e:
        return None, str(e)


def send_message(
    task_id: int,
    task: TASK_TYPE,
    data: Optional[UploadDataModel] = None,
):
    try:
        message = KafkaTaskMessageModel(task_id=task_id, task=task, data=data)

        producer = get_kafka_producer()
        producer.init_transactions()
        producer.begin_transaction()

        producer.produce(APISettings.KAFKA["TOPIC"], value=message.model_dump_json())

        producer.commit_transaction()

        del producer

        return True, None
    except Exception as e:
        return False, str(e)


def manage_new_task(task_type: TASK_TYPE, data=None):
    try:
        task, error = create_task(task_type)

        if not task:
            raise Exception(error)

        sended, error = send_message(task["id"], task_type, data=data)

        if not sended:
            raise Exception(error)

        return TaskResponseModel(
            message=NEW_TASK_SUCCESS_MESSAGE(task["id"], task["name"]),
            task_id=task["id"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorModel(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_type=ResponseErrorTypeEnum.HTTP_500,
                message=ResponseErrorMessage.HTTP_500,
                details=str(e),
            ).model_dump(),
        )
