from viva_vdm.core.models.models import JobStatuses
from viva_vdm.core.tasks.iedb_mhcii import mhcii_task
from viva_vdm.v1.models import CreateJobRequest
from viva_vdm.core.models import JobDBModel, HCSDBModel

from viva_vdm.core.tasks import blast_task, prosite_task, mhci_task


class CreateJobHelper(object):
    def __init__(self, payload: CreateJobRequest):
        self.job_instance = self._create_db_entry(payload)

    @classmethod
    def _create_db_entry(cls, payload: CreateJobRequest) -> JobDBModel:
        payload_dict = payload.dict()
        hcs_instances = [HCSDBModel(**hcs).save() for hcs in payload_dict.pop('hcs')]

        return JobDBModel(hcs=hcs_instances, **payload_dict).save()

    def process_hcs_blast(self):
        for hcs in self.job_instance.hcs:
            blast_task(hcs.id)

    def process_hcs_prosite(self):
        for hcs in self.job_instance.hcs:
            prosite_task(hcs.id)

    def process_hcs_mhci(self):
        for hcs in self.job_instance.hcs:
            mhci_task(hcs.id)

    def process_hcs_mhcii(self):
        for hcs in self.job_instance.hcs:
            mhcii_task(hcs.id)

    def _update_job_status(self):
        self.job_instance.status = JobStatuses.starting
        self.job_instance.save()

    def process(self) -> str:
        self._update_job_status()

        self.process_hcs_blast()
        self.process_hcs_prosite()
        self.process_hcs_mhci()
        self.process_hcs_mhcii()

        return self.job_instance.id
