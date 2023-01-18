from viva_vdm.core.celery_app import app
from viva_vdm.core.iedb.mhcii.constants import MhcIISupertypes
from viva_vdm.core.iedb.mhcii.factory import MhcIIPredictionFactory
from viva_vdm.core.models import (
    LoggerContexts,
    LoggerFlags,
    LoggerMessages,
    HCSStatuses,
    HCSDBModel,
)

from viva_vdm.core.models.models import MHCIISupertypes


@app.task(name='MHCII')
def mhcii_task(hcs_id: str):
    """
    This is the Celery task for Blast analysis.

    :param hcs_id: A valid HCS from the provided job name.
    :type hcs_id: str
    """

    # We get the queryset (ie: use filter) so we can update the logs easier
    hcs_qs = HCSDBModel.objects.filter(id=hcs_id)
    hcs = hcs_qs.get()

    if hcs.status.mhcii == HCSStatuses.completed:
        return

    hcs_qs.update_log(LoggerContexts.mhcii, LoggerFlags.info, LoggerMessages.MHCII_STARTING)
    hcs.status.mhcii = HCSStatuses.running

    mhcii_prediction_method = hcs.mhcii_prediction_method.value
    supertype_results = dict()

    for supertype in MhcIISupertypes:
        results = MhcIIPredictionFactory(supertype=supertype, method=mhcii_prediction_method).predict(hcs.sequence)
        supertype_results[supertype.name] = [result.dict() for result in results]

    hcs.results.mhcii = MHCIISupertypes(**supertype_results)

    hcs_qs.update_log(LoggerContexts.mhcii, LoggerFlags.error, LoggerMessages.MHCII_COMPLETED)
    hcs.status.mhcii = HCSStatuses.completed

    hcs.save()
