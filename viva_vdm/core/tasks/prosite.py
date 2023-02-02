from viva_vdm.core.prosite.exceptions import PrositeError
from viva_vdm.core.prosite.wrapper import PrositeScan
from viva_vdm.core.celery_app import app
from viva_vdm.core.models import (
    LoggerContexts,
    LoggerFlags,
    LoggerMessages,
    HCSDBModel,
    PrositeDBModel,
    JobDBModel,
)


def prosite_hcs(hcs_id: str):
    """
    This is the Celery task for prosite analysis.

    :param hcs_id: A valid HCS from the provided job name.
    :type hcs_id: str
    """

    hcs = HCSDBModel.objects.get(id=hcs_id)
    results = PrositeScan(output_xpsa=True, cutoff_value=-1, is_fasta=True, show_prof_start_end=True).scan(hcs.sequence)

    hcs.results.prosite = [
        PrositeDBModel(accession=result.accession, description=result.description, start=result.start, end=result.end)
        for result in results
    ]

    hcs.save()


@app.task(name='Prosite')
def prosite_task(job_id: str):
    job = JobDBModel.objects.get(id=job_id)
    JobDBModel.objects.update_log(job_id, LoggerContexts.blast, LoggerFlags.info, LoggerMessages.PROSITE_STARTING)

    for hcs in job.hcs:
        try:
            prosite_hcs(hcs.id)
        except PrositeError as ex:
            JobDBModel.objects.update_log(
                job_id, LoggerContexts.prosite, LoggerFlags.error, LoggerMessages.PROSITE_ERROR
            )
            raise ex

    JobDBModel.objects.update_log(job_id, LoggerContexts.blast, LoggerFlags.info, LoggerMessages.PROSITE_COMPLETED)
