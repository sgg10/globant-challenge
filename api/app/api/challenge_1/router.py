from fastapi import Body, status, APIRouter, HTTPException

from app.api.models import ErrorModel
from app.api.challenge_1.models import UploadDataModel

router = APIRouter(prefix="/challenge_1", tags=["challenge_1"])


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    summary="Upload data for departments, jobs, or employees",
)
def upload_data(body: UploadDataModel = Body(...)):
    if not body.has_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorModel(
                code=status.HTTP_400_BAD_REQUEST,
                message="Bad Request",
                error_type="NO_DATA_PROVIDED",
                details="No data provided",
            ).model_dump(),
        )

    if not body.complies_data_size_limit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorModel(
                code=status.HTTP_400_BAD_REQUEST,
                message="Data size limit exceeded",
                error_type="DATA_SIZE_LIMIT_EXCEEDED",
                details="The data size limit is 1000 records per entity",
            ).model_dump(),
        )

    try:
        return {"message": "Data uploaded successfully", "data": body}
    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorModel(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_type="INTERNAL_SERVER_ERROR",
                message="Internal server error",
                details=str(e),
            ).model_dump(),
        )


@router.post(
    path="/backup",
    status_code=status.HTTP_201_CREATED,
    summary="Backup data for departments, jobs, or employees",
)
def backup_task(body=Body(...)):
    return {"message": "Data backup successfully", "data": body}


@router.post(
    path="/restore",
    status_code=status.HTTP_201_CREATED,
    summary="Restore data for departments, jobs, or employees",
)
def restore_task(body=Body(...)):
    return {"message": "Data restore successfully", "data": body}
