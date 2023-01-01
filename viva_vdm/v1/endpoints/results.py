from fastapi import APIRouter, status, HTTPException
from mongoengine import DoesNotExist

from ..models import CreateJobRequest, JobLogs, JobLogEntry, JobParameters
from ..helpers import HelperMethods
from ...core.models import JobStatus

router = APIRouter(prefix='/job', tags=['job'])


@router.post('/create', status_code=status.HTTP_201_CREATED, response_description="Returns the auto-generated job id.")
def create_job(payload: CreateJobRequest) -> str:
    """
    Submit a new standalone analysis job.

    A successful request will return a HTTP 201 status code, while any invalid request (missing fields) will return
    an HTTP 500 status code with the body indicating the missing fields.
    """

    job_id = HelperMethods.create_job(payload)

    return job_id


@router.get(
    '/status/{job_id}',
    status_code=status.HTTP_200_OK,
    response_description="Returns the current status of the job",
    response_model=JobStatus,
)
def get_job_status(job_id: str) -> JobStatus:
    """
    Get the status of a job.

    If the provided job id is not found an HTTP 404 status is returned. A successful request will return an HTTP 200.
    """

    try:
        job = HelperMethods.get_job(job_id)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found, consider creating one.")

    return job.status


@router.get(
    '/log/{job_id}',
    status_code=status.HTTP_200_OK,
    response_description="Returns the current status of the job",
    response_model=JobLogs,
)
def get_job_log(job_id: str) -> JobLogs:
    """
    Get the logs of a job.

    If the provided job id is not found an HTTP 404 status is returned. A successful request will return an HTTP 200.
    """

    try:
        job = HelperMethods.get_job(job_id)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found, consider creating one.")

    entries = [JobLogEntry(**entry.to_mongo().to_dict()) for entry in job.log]

    return JobLogs(logs=entries)


@router.get(
    '/parameters/{job_id}',
    status_code=status.HTTP_200_OK,
    response_description="Returns the parameters that were used to run the job",
    response_model=JobParameters,
)
def get_job_parameters(job_id: str) -> JobParameters:
    """
    Get the parameters that were used to run the job.

    If the provided job id is not found an HTTP 404 status is returned. A successful request will return an HTTP 200.
    """

    try:
        job = HelperMethods.get_job(job_id)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found, consider creating one.")

    return JobParameters(**job.parameters.to_mongo().to_dict())
