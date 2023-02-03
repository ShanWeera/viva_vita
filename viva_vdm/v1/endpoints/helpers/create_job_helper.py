from viva_vdm.core.tasks.job import vita_job
from viva_vdm.v1.models import CreateJobRequest
from viva_vdm.core.models import JobDBModel, HCSDBModel


class CreateJobHelper(object):
    def __init__(self, payload: CreateJobRequest):
        self.job_instance = self._create_db_entry(payload)

    @classmethod
    def _create_db_entry(cls, payload: CreateJobRequest) -> JobDBModel:
        payload_dict = payload.dict()
        hcs_instances = [HCSDBModel(**hcs).save() for hcs in payload_dict.pop('hcs')]

        return JobDBModel(hcs=hcs_instances, **payload_dict).save()

    def create_and_process(self) -> str:
        vita_job.delay(self.job_instance.id)

        return self.job_instance.id
