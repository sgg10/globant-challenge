from fastapi import status, APIRouter, HTTPException, Path


from app.core import constants
from app.api.utils import manage_new_task
from app.api.challenge_2.models import ReportTypeModel
from app.api.models import ErrorModel, TaskResponseModel


router = APIRouter(
    prefix=f"/{constants.CHALLENGE_2_PREFIX}", tags=[constants.CHALLENGE_2_PREFIX]
)


@router.get(
    path=constants.CHALLENGE_2_REPORT_ENDPOINT,
    status_code=status.HTTP_200_OK,
    summary=constants.CHALLENGE_2_REPORT_ENDPOINT_SUMMARY,
    response_model=TaskResponseModel,
)
def get_report(type: str = Path(...)):
    """
    # Get Report

    Get a report based on the specified report type (`type1` or `type2`).

    ## Parameters:
        type (str): The type of the report.

    ## Returns:
        TaskResponseModel: The response model containing the task information.

    ## Raises:
        HTTPException: If the specified report does not exist.

    """

    try:
        report_type = ReportTypeModel(report_type=type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorModel(
                code=status.HTTP_404_NOT_FOUND,
                message=constants.ResponseErrorMessage.REPORT_NOT_FOUND,
                error_type=constants.ResponseErrorTypeEnum.REPORT_NOT_FOUND,
                details=constants.ResponseErrorMessage.REPORT_NOT_FOUND,
            ).model_dump(),
        )

    return manage_new_task(constants.TaskTypeEnum.REPORT.value, data=report_type)
