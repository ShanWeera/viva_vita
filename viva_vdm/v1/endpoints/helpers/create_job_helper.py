from celery import chord

from viva_vdm.core.tasks.complete_job import complete_job
from viva_vdm.core.tasks.iedb_mhcii import mhcii_task
from viva_vdm.v1.models import CreateJobRequest
from viva_vdm.core.models import JobDBModel, HCSDBModel, LoggerContexts, LoggerFlags, LoggerMessages

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
        blast_task.delay(str(self.job_instance.id))

    def process_hcs_prosite(self):
        prosite_task.delay(str(self.job_instance.id))

    def process_hcs_mhci(self):
        mhci_task.delay(str(self.job_instance.id))

    def process_hcs_mhcii(self):
        mhcii_task.delay(str(self.job_instance.id))

    def process(self) -> str:
        JobDBModel.objects.update_log(
            str(self.job_instance.id), LoggerContexts.general, LoggerFlags.info, LoggerMessages.JOB_STARTING
        )

        tasks = (
            blast_task.s(str(self.job_instance.id)),
            prosite_task.s(str(self.job_instance.id)),
            mhci_task.s(str(self.job_instance.id)),
            mhcii_task.s(str(self.job_instance.id)),
        )

        chord(tasks)(complete_job.s())

        return self.job_instance.id
