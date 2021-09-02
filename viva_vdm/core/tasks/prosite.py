from ..prosite.exceptions import PrositeError
from ..prosite.wrapper import PrositeScan
from ..celery_app import app
from ..models.models import (
    PrositeDBModel,
    HCSResultsDBModel,
    HCSDBModel,
    LoggerContexts,
    LoggerFlags,
    LoggerMessages,
    HCSStatuses,
)


@app.task(name='Prosite')
def prosite_task(hcs_id: str):
    """
    This is the Celery task for prosite analysis.

    :param hcs_id: A valid HCS from the provided job name.
    :type hcs_id: str
    """

    # We get the queryset so we can update the logs easier
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

    prosite_model = [
        PrositeDBModel(accession=result.accession, description=result.description, start=result.start, end=result.end)
        for result in results
    ]
    results_model = HCSResultsDBModel(prosite=prosite_model)

    # We update the log to indicate that we are done
    hcs_qs.update_log(LoggerContexts.prosite, LoggerFlags.error, LoggerMessages.PROSITE_COMPLETED)

    # We update the status to indicate this HCS has gone through Prosite analysis successfully
    hcs.status.prosite = HCSStatuses.completed

    # We then save it to the hcs instance
    hcs.results = results_model
    hcs.save()
