from viva_vdm.core.celery_app import app
from viva_vdm.core.models import (
    LoggerContexts,
    LoggerFlags,
    LoggerMessages,
    HCSStatuses,
    HCSDBModel,
)

from viva_vdm.core.iedb.mhci.constants import MhcISupertypes
from viva_vdm.core.iedb.mhci.factory import MhcIPredictionFactory
from viva_vdm.core.models.models import MHCISupertypes


@app.task(name='MHCI')
def mhci_task(hcs_id: str):
    """
    This is the Celery task for Blast analysis.

    :param hcs_id: A valid HCS from the provided job name.
    :type hcs_id: str
    """

    # We get the queryset (ie: use filter) so we can update the logs easier
    hcs_qs = HCSDBModel.objects.filter(id=hcs_id)
    hcs = hcs_qs.get()

    if hcs.status.mhci == HCSStatuses.completed:
        return

    hcs_qs.update_log(LoggerContexts.mhci, LoggerFlags.info, LoggerMessages.MHCI_STARTING)
    hcs.status.mhci = HCSStatuses.running

    mhci_prediction_method = hcs.mhci_prediction_method.value
    supertype_results = dict()

    for supertype in MhcISupertypes:
        results = MhcIPredictionFactory(supertype=supertype, method=mhci_prediction_method).predict(hcs.sequence)
        supertype_results[supertype.name] = [result.dict() for result in results]

    hcs.results.mhci = MHCISupertypes(**supertype_results)

    hcs_qs.update_log(LoggerContexts.mhci, LoggerFlags.error, LoggerMessages.MHCI_COMPLETED)
    hcs.status.mhci = HCSStatuses.completed

    hcs.save()
