from ..blast.exceptions import BlastException
from ..blast.wrapper import BlastCliWrapper
from ..celery_app import app
from ..models.models import (
    HCSResultsDBModel,
    HCSDBModel,
    LoggerContexts,
    LoggerFlags,
    LoggerMessages,
    HCSStatuses,
    BlastDBModel,
)
from ..blast.models import BlastResults


@app.task(name='Blast')
def blast_task(hcs_id: str):
    """
    This is the Celery task for Blast analysis.

    :param hcs_id: A valid HCS from the provided job name.
    :type hcs_id: str
    """

    # We get the queryset so we can update the logs easier
    hcs_qs = HCSDBModel.objects.filter(id=hcs_id)

    # We then retrieve the job from the database
    hcs = hcs_qs.get()

    # If Blast analysis has already been done, we exit gracefully
    if hcs.status.blast == HCSStatuses.completed:
        return

    # We then update the log, and status to inform we are starting analysis
    hcs_qs.update_log(LoggerContexts.prosite, LoggerFlags.info, LoggerMessages.PROSITE_STARTING)
    hcs.status.blast = HCSStatuses.running

    # We then get the HCS sequence, and run Blast analysis
    try:
        result = BlastCliWrapper().run_blast(hcs.sequence)  # type: BlastResults
    except BlastException as ex:
        # Update the log to indicate error
        hcs_qs.update_log(LoggerContexts.prosite, LoggerFlags.error, LoggerMessages.BLAST_ERROR)
        hcs.status.blast = HCSStatuses.failed

        raise ex

    blast_model_entries = list()

    for hit in result.BlastOutput2[0].report.results.search.hits:
        for desc in hit.description:
            sciname = desc.sciname
            strain = None

            if not sciname.isalnum():  # Strain name is included in scientific name
                paranthesis_start = sciname.find("(") + 1
                paranthesis_end = sciname.find(")", len(sciname) - 1)

                strain = sciname[paranthesis_start:paranthesis_end]

            blast_model_entries.append(
                BlastDBModel(accession=desc.accession, species=desc.sciname, strain=strain, taxid=desc.taxid)
            )

    results_model = HCSResultsDBModel(blast=blast_model_entries)

    # We update the log to indicate that we are done
    hcs_qs.update_log(LoggerContexts.blast, LoggerFlags.info, LoggerMessages.BLAST_COMPLETED)

    # We update the status to indicate this HCS has gone through Blast analysis successfully
    hcs.status.blast = HCSStatuses.completed

    # We then save it to the hcs instance
    hcs.results = results_model
    hcs.save()
