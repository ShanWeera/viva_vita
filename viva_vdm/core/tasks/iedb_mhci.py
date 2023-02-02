from viva_vdm.core.celery_app import app
from viva_vdm.core.models import (
    LoggerContexts,
    LoggerFlags,
    LoggerMessages,
    HCSDBModel,
)

from viva_vdm.core.iedb.mhci.constants import MhcISupertypes
from viva_vdm.core.iedb.mhci.factory import MhcIPredictionFactory
from viva_vdm.core.models.models import MHCISupertypes, JobDBModel, MHCIPredictionMethods


@app.task(name='MHCI')
def mhci_hcs(hcs_id: str, prediction_method: MHCIPredictionMethods):
    """
    This is the Celery task for Blast analysis.

    :param hcs_id: A valid HCS from the provided job name.
    :type hcs_id: str

    :param prediction_method: The prediction method to use
    :type prediction_method: MHCIPredictionMethods
    """

    hcs = HCSDBModel.objects.get(id=hcs_id)

    supertype_results = dict()
    for supertype in MhcISupertypes:
        results = MhcIPredictionFactory(supertype=supertype, method=prediction_method.value).predict(hcs.sequence)
        supertype_results[supertype.name] = [result.dict() for result in results]

    hcs.results.mhci = MHCISupertypes(**supertype_results)

    hcs.save()


@app.task(name='MHCI')
def mhci_task(job_id: str):
    job = JobDBModel.objects.get(id=job_id)
    JobDBModel.objects.update_log(job_id, LoggerContexts.mhci, LoggerFlags.info, LoggerMessages.MHCI_STARTING)

    for hcs in job.hcs:
        try:
            mhci_hcs(hcs.id, job.mhci_prediction_method)
        except Exception as ex:
            JobDBModel.objects.update_log(job_id, LoggerContexts.mhci, LoggerFlags.error, LoggerMessages.MHCI_ERROR)
            raise ex

    JobDBModel.objects.update_log(job_id, LoggerContexts.mhci, LoggerFlags.info, LoggerMessages.MHCI_COMPLETED)
