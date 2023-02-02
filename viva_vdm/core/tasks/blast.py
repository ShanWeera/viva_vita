from viva_vdm.core.blast.exceptions import BlastException
from viva_vdm.core.blast.wrapper import BlastCliWrapper
from viva_vdm.core.celery_app import app
from viva_vdm.core.models import (
    HCSResultsDBModel,
    LoggerContexts,
    LoggerFlags,
    LoggerMessages,
    BlastDBModel,
    HCSDBModel,
    JobDBModel,
)
from viva_vdm.core.blast.models import BlastResults


def blast_hcs(hcs_id: str, taxonomy_id: int):
    """
    This is the Celery task for Blast analysis.

    :param hcs_id: A valid HCS from the provided job name.
    :type hcs_id: str

    :param taxonomy_id: The taxonomy ID of the HCS
    :type taxonomy_id: int
    """

    hcs = HCSDBModel.objects.get(id=hcs_id)
    result = BlastCliWrapper(tax_ids_exclude=[taxonomy_id]).run_blast(hcs.sequence)  # type: BlastResults

    blast_model_entries = list()
    for hit in result.BlastOutput2[0].report.results.search.hits:
        for desc in hit.description:
            sciname = desc.sciname
            strain = None

            if sciname and not sciname.isalnum():  # Strain name is included in scientific name
                parentheses_start = sciname.find("(") + 1
                parentheses_end = sciname.find(")", len(sciname) - 1)

                strain = sciname[parentheses_start:parentheses_end]

            blast_model_entries.append(
                BlastDBModel(
                    accession=desc.accession, species=sciname, strain=strain, taxid=desc.taxid, title=desc.title
                )
            )

    results_model = HCSResultsDBModel(blast=blast_model_entries)

    hcs.results = results_model
    hcs.save()


@app.task(name='Blast')
def blast_task(job_id: str):
    job = JobDBModel.objects.get(id=job_id)
    JobDBModel.objects.update_log(job_id, LoggerContexts.blast, LoggerFlags.info, LoggerMessages.BLAST_STARTING)

    for hcs in job.hcs:
        try:
            blast_hcs(hcs.id, job.taxonomy_id)
        except BlastException as ex:
            JobDBModel.objects.update_log(job_id, LoggerContexts.blast, LoggerFlags.error, LoggerMessages.BLAST_ERROR)
            raise ex

    JobDBModel.objects.update_log(job_id, LoggerContexts.blast, LoggerFlags.info, LoggerMessages.BLAST_COMPLETED)
