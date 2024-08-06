from fastapi import Body, status, APIRouter, HTTPException

from app.core import constants
from app.api.models import ErrorModel
from app.api.utils import manage_new_task
from app.api.models import TaskResponseModel
from app.api.challenge_1.models import UploadDataModel, TableNameModel


router = APIRouter(
    prefix=f"/{constants.CHALLENGE_1_PREFIX}", tags=[constants.CHALLENGE_1_PREFIX]
)


@router.post(
    path=constants.CHALLENGE_1_UPLOAD_ENDPOINT,
    status_code=status.HTTP_201_CREATED,
    summary=constants.CHALLENGE_1_UPLOAD_ENDPOINT_SUMMARY,
    response_model=TaskResponseModel,
)
def upload_data(body: UploadDataModel = Body(...)):
    """
    # Upload Data

    This endpoint is used to upload data to the database.
    It creates a new task of type `LOAD` and returns the task response model.

    ## Parameters:
        body (UploadDataModel): The data to be uploaded.

    ## Raises:
        HTTPException: If the request body does not have data or exceeds the data size limit.

    ## Returns:
        TaskResponseModel: The response containing the newly created task.
    """
    if not body.has_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorModel(
                code=status.HTTP_400_BAD_REQUEST,
                message=constants.ResponseErrorMessage.NO_DATA_PROVIDED,
                error_type=constants.ResponseErrorTypeEnum.NO_DATA_PROVIDED,
                details=constants.ResponseErrorMessage.NO_DATA_PROVIDED,
            ).model_dump(),
        )

    if not body.complies_data_size_limit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorModel(
                code=status.HTTP_400_BAD_REQUEST,
                message=constants.ResponseErrorMessage.DATA_SIZE_LIMIT_EXCEEDED,
                error_type=constants.ResponseErrorTypeEnum.DATA_SIZE_LIMIT_EXCEEDED,
                details=constants.ResponseErrorMessage.DATA_SIZE_LIMIT_EXCEEDED,
            ).model_dump(),
        )

    return manage_new_task(constants.TaskTypeEnum.LOAD.value, data=body)


@router.post(
    path=constants.CHALLENGE_1_BACKUP_ENDPOINT,
    status_code=status.HTTP_201_CREATED,
    summary=constants.CHALLENGE_1_BACKUP_ENDPOINT_SUMMARY,
    response_model=TaskResponseModel,
)
def backup_task(body: TableNameModel = Body(...)):
    """
    # Backup a task.

    This endpoint is used to backup table.
    It creates a new task of type `BACKUP` and returns the task response model.

    ## Returns:
        TaskResponseModel: The response model containing the details of the new task.

    """
    return manage_new_task(constants.TaskTypeEnum.BACKUP.value, data=body)


@router.post(
    path=constants.CHALLENGE_1_RESTORE_ENDPOINT,
    status_code=status.HTTP_201_CREATED,
    summary=constants.CHALLENGE_1_RESTORE_ENDPOINT_SUMMARY,
    response_model=TaskResponseModel,
)
def restore_task(body: TableNameModel = Body(...)):
    """
    # Restore a task.

    This endpoint is used to restore data from last table backup.
    It creates a new task of type `RESTORE` and returns the task response model.

    ## Returns:
        TaskResponseModel: The response model containing the restored task.
    """
    return manage_new_task(constants.TaskTypeEnum.RESTORE.value, data=body)
