from typing import List

from fastapi import APIRouter, status, HTTPException
from mongoengine.errors import DoesNotExist

from viva_vdm.core.models import JobDBModel
from viva_vdm.core.models.models import JobStatuses
from viva_vdm.v1.models import CreateJobRequest, JobHCSListModel
from viva_vdm.v1.endpoints.helpers import CreateJobHelper

router = APIRouter(prefix='/job', tags=['job'])


@router.post('/create', status_code=status.HTTP_201_CREATED, response_description="Returns the auto-generated job id.")
def create_job(payload: CreateJobRequest) -> str:
    """
    Submit a new standalone analysis job.

    A successful request will return a HTTP 201 status code, while any invalid request (missing fields) will return
    an HTTP 500 status code with the body indicating the missing fields.
    """

    job_id = CreateJobHelper(payload).create_and_process()

    return job_id


@router.get(
    '/{job_id}/status',
    status_code=status.HTTP_200_OK,
    response_description="Returns the current status of the job",
    response_model=JobStatuses,
)
def get_job_status(job_id: str) -> JobStatuses:
    """
    Get the status of a job.

    If the provided job id is not found an HTTP 404 status is returned. A successful request will return an HTTP 200.
    """

    try:
        job_status = JobDBModel.objects.get(id=job_id).status
        return job_status
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found, consider creating one.")


@router.get(
    '/{job_id}/hcs',
    status_code=status.HTTP_200_OK,
    response_description="Returns a list of HCS for the job ID provide",
    response_model=List[JobHCSListModel],
)
def get_job_hcs(job_id: str) -> List[JobHCSListModel]:
    """
    Get a list of HCS for the job ID

    If the provided job id is not found an HTTP 404 status is returned. A successful request will return an HTTP 200.
    """

    try:
        job = JobDBModel.objects.get(id=job_id)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found, consider creating one.")

    return [JobHCSListModel(**hcs.to_mongo().to_dict()) for hcs in job.hcs]
