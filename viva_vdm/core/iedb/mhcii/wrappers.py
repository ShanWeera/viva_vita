from viva_vdm.core.iedb.common.predictor_base import PredictorBase
from viva_vdm.core.iedb.mhci.utils import run_mhcii_prediction_process


class MHCIIPredictorBase(PredictorBase):
    def run_prediction_process(self, allele: str, sequence: str) -> tuple[str, str]:
        return run_mhcii_prediction_process(self.method, allele, self.length, sequence)


class MhcIINetMhcPan(MHCIIPredictorBase):
    def get_table_template(self):
        return """
<group>
{{ allele }} {{ seq_num }} {{ start | to_int }} {{ end | to_int }} {{ length | to_int }} {{ sequence }} {{ _peptide }} {{ ic50 | to_float }} {{ percentile | to_float}} {{ _percentile | to_float }}
</group>
"""  # noqa: E501


class MhcIIConsensus(MHCIIPredictorBase):
    def get_table_template(self):
        return """
<group>
{{ allele }} {{ ignore }} {{ start }} {{ end }} {{ length | to_int }} {{ sequence }} {{ percentile | to_float }} {{ ignore }} {{ ignore }} {{ ignore }} {{ ignore }} {{ ignore }} {{ ignore }} {{ ignore }} {{ ignore }} {{ ignore }} {{ ignore }} {{ ignore }} {{ ignore }} {{ ignore }} {{ ignore }} {{ ignore }} {{ ignore }} {{ ignore }}
</group>
"""  # noqa: E501


class MhcIINnAlign(MHCIIPredictorBase):
    def get_table_template(self):
        return """
<group>
{{ allele }} {{ seq_num }} {{ start | to_int }} {{ end | to_int }} {{ length | to_int }} {{ sequence }} {{ _peptide }} {{ ic50 | to_float }} {{ percentile | to_float}} {{ _percentile | to_float }}
</group>
"""  # noqa: E501


class MhcIISmmAlign(MHCIIPredictorBase):
    def get_table_template(self):
        return """
<group>
{{ allele }} {{ seq_num }} {{ start | to_int }} {{ end | to_int }} {{ length | to_int }} {{ sequence }} {{ _peptide }} {{ ic50 | to_float }} {{ percentile | to_float}} {{ _percentile | to_float }}
</group>
"""  # noqa: E501


class MhcIICombLib(MHCIIPredictorBase):
    def get_table_template(self):
        return """
<group>
{{ allele }} {{ seq_num }} {{ start | to_int }} {{ end | to_int }} {{ length | to_int }} {{ sequence }} {{ _peptide }} {{ ic50 | to_float }} {{ percentile | to_float}} {{ _percentile | to_float }}
</group>
"""  # noqa: E501


class MhcIINetMhcPanEl(MHCIIPredictorBase):
    def get_table_template(self):
        return """
<group>
{{ allele }} {{ seq_num }} {{ start | to_int }} {{ end | to_int }} {{ length | to_int }} {{ sequence }} {{ _peptide }} {{ ic50 | to_float }} {{ percentile | to_float}}
</group>
"""  # noqa: E501


class MhcIINetMhcPanBa(MHCIIPredictorBase):
    def get_table_template(self):
        return """
<group>
{{ allele }} {{ seq_num }} {{ start | to_int }} {{ end | to_int }} {{ length | to_int }} {{ sequence }} {{ _peptide }} {{ ic50 | to_float }} {{ percentile | to_float}}
</group>
"""  # noqa: E501
