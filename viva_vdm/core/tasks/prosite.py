from ..prosite.exceptions import PrositeError
from ..prosite.wrapper import PrositeScan
from ..celery_app import app
from viva_vdm.core.models import (
    LoggerContexts,
    LoggerFlags,
    LoggerMessages,
    HCSStatuses,
    HCSDBModel,
    PrositeDBModel,
)


@app.task(name='Prosite')
def prosite_task(hcs_id: str):
    """
    This is the Celery task for prosite analysis.

    :param hcs_id: A valid HCS from the provided job name.
    :type hcs_id: str
    """

    # We get the queryset (ie: use filter) so we can update the logs easier
    hcs_qs = HCSDBModel.objects.filter(id=hcs_id)

    # We then retrieve the job from the database
    hcs = hcs_qs.get()

    # If Prosite analysis has already been done, we exit gracefully
    if hcs.status.prosite == HCSStatuses.completed:
        return

    # We then update the log, and status to inform we are starting analysis
    hcs_qs.update_log(LoggerContexts.prosite, LoggerFlags.info, LoggerMessages.PROSITE_STARTING)
    hcs.status.prosite = HCSStatuses.running

    # We then get the HCS sequence, and run Prosite analysis
    try:
        results = PrositeScan(output_xpsa=True, cutoff_value=-1, is_fasta=True, show_prof_start_end=True).scan(
            hcs.sequence
        )
    except PrositeError as ex:
        # Update the log to indicate error
        hcs_qs.update_log(LoggerContexts.prosite, LoggerFlags.error, LoggerMessages.PROSITE_ERROR)
        hcs.status.prosite = HCSStatuses.failed

        raise ex

    hcs.results.prosite = [
        PrositeDBModel(accession=result.accession, description=result.description, start=result.start, end=result.end)
        for result in results
    ]

    hcs_qs.update_log(LoggerContexts.prosite, LoggerFlags.error, LoggerMessages.PROSITE_COMPLETED)
    hcs.status.prosite = HCSStatuses.completed

    hcs.save()
