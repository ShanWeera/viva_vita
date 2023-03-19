from viva_vdm.core.celery_app import app
from viva_vdm.core.workflow.vita_workflow import VitaWorkflow


@app.task(name='Job')
def vita_job(job_id: str):
    VitaWorkflow(job_id=job_id).process()
