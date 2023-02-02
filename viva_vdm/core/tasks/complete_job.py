from viva_vdm.core.celery_app import app
from viva_vdm.core.models import JobDBModel, LoggerContexts, LoggerFlags, LoggerMessages
from viva_vdm.core.models.models import JobStatuses


@app.task(name='CompleteJob')
def complete_job(job_id: str):
    job = JobDBModel.objects.update_log(job_id, LoggerContexts.general, LoggerFlags.info, LoggerMessages.JOB_COMPLETED)
    job.status = JobStatuses.completed
    job.save()
