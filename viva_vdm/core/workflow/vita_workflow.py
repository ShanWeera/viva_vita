from typing import Optional

from viva_vdm.core.blast import BlastCliWrapper
from viva_vdm.core.iedb.mhci.constants import MhcISupertypes
from viva_vdm.core.iedb.mhci.factory import MhcIPredictionFactory
from viva_vdm.core.iedb.mhcii.constants import MhcIISupertypes
from viva_vdm.core.iedb.mhcii.factory import MhcIIPredictionFactory
from viva_vdm.core.models import (
    JobDBModel,
    HCSDBModel,
    BlastDBModel,
    HCSResultsDBModel,
    PrositeDBModel,
    MHCIPredictionMethods,
)
from viva_vdm.core.blast.models import BlastResults
from viva_vdm.core.models.models import (
    MHCISupertypes,
    MHCIIPredictionMethods,
    MHCIISupertypes,
    JobStatuses,
    LoggerContexts,
    LoggerFlags,
    LoggerMessages,
)
from viva_vdm.core.prosite import PrositeScan
from viva_vdm.core.workflow.decorators import handle_feedback


class VitaWorkflow(object):
    def __init__(self, job_id: Optional[str] = None, job_instance: Optional[JobDBModel] = None):
        self.job_instance = job_instance or self._get_job_instance(job_id)

    @classmethod
    def _get_job_instance(cls, job_id: str):
        return JobDBModel.objects.get(id=job_id)

    def _convey_job_start(self):
        JobDBModel.objects.update_status(instance=self.job_instance, status=JobStatuses.started)
        JobDBModel.objects.update_log(
            instance=self.job_instance,
            context=LoggerContexts.general,
            flag=LoggerFlags.info,
            msg=LoggerMessages.JOB_RUNNING,
        )

    def _convey_job_end(self):
        JobDBModel.objects.update_status(instance=self.job_instance, status=JobStatuses.completed)
        JobDBModel.objects.update_log(
            instance=self.job_instance,
            context=LoggerContexts.general,
            flag=LoggerFlags.info,
            msg=LoggerMessages.JOB_COMPLETED,
        )

    @handle_feedback(context=LoggerContexts.blast)
    def _run_blast_for_hcs(self, hcs: HCSDBModel, taxonomy_id: int):
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

    @handle_feedback(context=LoggerContexts.prosite)
    def _run_prosite_for_hcs(self, hcs: HCSDBModel):
        results = PrositeScan(output_xpsa=True, cutoff_value=-1, is_fasta=True, show_prof_start_end=True).scan(
            hcs.sequence
        )

        hcs.results.prosite = [
            PrositeDBModel(
                accession=result.accession, description=result.description, start=result.start, end=result.end
            )
            for result in results
        ]

        hcs.save()

    @handle_feedback(context=LoggerContexts.mhci)
    def _run_mhci_for_hcs(self, hcs: HCSDBModel, prediction_method: MHCIPredictionMethods):
        supertype_results = dict()
        for supertype in MhcISupertypes:
            results = MhcIPredictionFactory(supertype=supertype, method=prediction_method.value).predict(hcs.sequence)
            supertype_results[supertype.name] = [result.dict() for result in results]

        hcs.results.mhci = MHCISupertypes(**supertype_results)
        hcs.save()

    @handle_feedback(context=LoggerContexts.mhcii)
    def _run_mhcii_for_hcs(self, hcs: HCSDBModel, prediction_method: MHCIIPredictionMethods):
        supertype_results = dict()
        for supertype in MhcIISupertypes:
            results = MhcIIPredictionFactory(supertype=supertype, method=prediction_method.value).predict(hcs.sequence)
            supertype_results[supertype.name] = [result.dict() for result in results]

        hcs.results.mhcii = MHCIISupertypes(**supertype_results)
        hcs.save()

    def process(self):
        if self.job_instance.status == JobStatuses.completed:
            return

        self._convey_job_start()

        for hcs in self.job_instance.hcs:
            self._run_prosite_for_hcs(hcs)
            self._run_mhci_for_hcs(hcs, self.job_instance.mhci_prediction_method)
            self._run_mhcii_for_hcs(hcs, self.job_instance.mhcii_prediction_method)
            self._run_blast_for_hcs(hcs, self.job_instance.taxonomy_id)

        self._convey_job_end()
