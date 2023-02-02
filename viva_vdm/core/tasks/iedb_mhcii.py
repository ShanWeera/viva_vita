from viva_vdm.core.celery_app import app
from viva_vdm.core.iedb.mhcii.constants import MhcIISupertypes
from viva_vdm.core.iedb.mhcii.factory import MhcIIPredictionFactory
from viva_vdm.core.models import (
    LoggerContexts,
    LoggerFlags,
    LoggerMessages,
    HCSDBModel,
)

from viva_vdm.core.models.models import MHCIISupertypes, MHCIIPredictionMethods, JobDBModel


@app.task(name='MHCII')
def mhcii_hcs(hcs_id: str, prediction_method: MHCIIPredictionMethods):
    """
    This is the Celery task for Blast analysis.

    :param hcs_id: A valid HCS from the provided job name.
    :type hcs_id: str

    :param prediction_method: Prediction method to use
    :type prediction_method: MHCIIPredictionMethods
    """

    hcs = HCSDBModel.objects.get(id=hcs_id)

    supertype_results = dict()
    for supertype in MhcIISupertypes:
        results = MhcIIPredictionFactory(supertype=supertype, method=prediction_method.value).predict(hcs.sequence)
        supertype_results[supertype.name] = [result.dict() for result in results]

    hcs.results.mhcii = MHCIISupertypes(**supertype_results)
    hcs.save()


@app.task(name='MHCII')
def mhcii_task(job_id: str):
    job = JobDBModel.objects.get(id=job_id)
    JobDBModel.objects.update_log(job_id, LoggerContexts.mhcii, LoggerFlags.info, LoggerMessages.MHCII_STARTING)

    for hcs in job.hcs:
        try:
            mhcii_hcs(hcs.id, job.mhcii_prediction_method)
        except Exception as ex:
            JobDBModel.objects.update_log(job_id, LoggerContexts.mhcii, LoggerFlags.error, LoggerMessages.MHCII_ERROR)
            raise ex

    JobDBModel.objects.update_log(job_id, LoggerContexts.mhcii, LoggerFlags.info, LoggerMessages.MHCII_COMPLETED)
