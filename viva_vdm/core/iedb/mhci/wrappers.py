from typing import TypedDict

from viva_vdm.core.iedb.common.predictor_base import PredictorBase
from .utils import run_mhci_prediction_process


ErrorType = TypedDict('ErrorType', {'allele': str, 'errors': str})


class MHCIPredictorBase(PredictorBase):
    def run_prediction_process(self, allele: str, sequence: str) -> tuple[str, str]:
        return run_mhci_prediction_process(self.method, allele, self.length, sequence)


class MhcINetMhcPan(MHCIPredictorBase):
    def get_table_template(self):
        return """
<group>
{{ allele }} {{ seq_num | to_int }} {{ start | to_int }} {{ end | to_int }} {{ length | to_int }} {{ sequence }} {{ core }} {{ icore }} {{ ic50 | to_float }} {{ percentile | to_float }}
</group>
"""  # noqa: E501


class MhcIANN(MHCIPredictorBase):
    def get_table_template(self):
        return """
<group>
{{ allele }} {{ seq_num | to_int }} {{ start | to_int }} {{ end | to_int }} {{ length | to_int }} {{ sequence }} {{ ic50 | to_float }} {{ percentile | to_float }}
</group>
"""  # noqa: E501


class MhcINetMhcPanEL(MhcINetMhcPan):
    def get_table_template(self):
        return """
<group>
{{ allele }} {{ seq_num | to_int }} {{ start | to_int }} {{ end | to_int }} {{ length | to_int }} {{ sequence }} {{ core }} {{ icore }} {{ score | to_float }} {{ percentile | to_float }}
</group>
"""  # noqa: E501


class MhcIPickpocket(MHCIPredictorBase):
    def get_table_template(self):
        return """
<group>
{{ allele }} {{ seq_num | to_int }} {{ start | to_int }} {{ end | to_int }} {{ length | to_int }} {{ sequence }} {{ ic50 | to_float }} {{ percentile | to_float }}
</group>
"""  # noqa: E501


class MhcISMM(MHCIPredictorBase):
    def get_table_template(self):
        return """
<group>
{{ allele }} {{ seq_num | to_int }} {{ start | to_int }} {{ end | to_int }} {{ length | to_int }} {{ sequence }} {{ ic50 | to_float }} {{ percentile | to_float }}
</group>
"""  # noqa: E501


class MhcISMMPMBEC(MHCIPredictorBase):
    def get_table_template(self):
        return """
<group>
{{ allele }} {{ seq_num | to_int }} {{ start | to_int }} {{ end | to_int }} {{ length | to_int }} {{ sequence }} {{ ic50 | to_float }} {{ percentile | to_float }}
</group>
"""  # noqa: E501


class MhcIConsensus(MHCIPredictorBase):
    def get_table_template(self):
        return """
<group>
{{ allele }} {{ seq_num | to_int }} {{ start | to_int }} {{ end | to_int }} {{ length | to_int }} {{ sequence }} {{ percentile | to_float }} {{ ignore }} {{ ignore }} {{ ignore }} {{ ignore }} {{ ignore }} {{ ignore }}
</group>
"""  # noqa: E501


class MhcINetMhcCons(MHCIPredictorBase):
    def get_table_template(self):
        return """
<group>
{{ allele }} {{ seq_num | to_int }} {{ start | to_int }} {{ end | to_int }} {{ length | to_int }} {{ sequence }} {{ ic50 | to_float }} {{ percentile | to_float }}
</group>
"""  # noqa: E501


class MhcINetMhcStabPan(MHCIPredictorBase):
    def get_table_template(self):
        return """
<group>
{{ allele }} {{ seq_num | to_int }} {{ start | to_int }} {{ end | to_int }} {{ length | to_int }} {{ sequence }} {{ ic50 | to_float }} {{ percentile | to_float }}
</group>
"""  # noqa: E501
