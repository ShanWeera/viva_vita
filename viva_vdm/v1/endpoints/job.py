from fastapi import APIRouter, status

from viva_vdm.v1.models import CreateJobRequest
from viva_vdm.v1.endpoints.helpers import CreateJobHelper

router = APIRouter(prefix='/job', tags=['job'])


@router.post('/create', status_code=status.HTTP_201_CREATED, response_description="Returns the auto-generated job id.")
def create_job(payload: CreateJobRequest) -> str:
    """
    Submit a new standalone analysis job.

    A successful request will return a HTTP 201 status code, while any invalid request (missing fields) will return
    an HTTP 500 status code with the body indicating the missing fields.
    """

    job_id = CreateJobHelper(payload).process()

    return job_id
