from typing import List, TypedDict

from ttp import ttp

from .utils import run_mhci_prediction_process
from .constants import MhcISupertypes, PredictionMethods
from .models import MHCIEpitope


ErrorType = TypedDict('ErrorType', {'allele': str, 'errors': str})


class MHCIPredictorBase(object):
    def __init__(
        self,
        *,
        supertype: MhcISupertypes,
        method: PredictionMethods = PredictionMethods.NETMHCPAN,
        length: int = 9,
        cutoff: float = 1.00,
    ):
        """
        This constructor is common for all MHC I prediction methods. It is recommended to not use this directly,
        but through the factory.

        :param supertype: A pre-defined MHC I supertype.
        :param method: One of the pre-defined MHC I prediction methods (default: NETMHCPAN).
        :param length: The length of the generated epitopes (default: 9).
        :param cutoff: The IEDB percentile cutoff (default: 1%).

        :type supertype: MhcISupertypes
        :type method: PredictionMethods
        :type length: int
        :type cutoff: float

        Example:
            >>> from viva_vdm.core.iedb.mhci.constants import MhcISupertypes, PredictionMethods
            >>> from viva_vdm.core.iedb.mhci.wrappers import MhcINetMhcPan
            >>> prediction_supertype = MhcISupertypes.A1
            >>> predictor = MhcINetMhcPan(prediction_supertype)
            >>> results = predictor.predict("MDSNTVSSFQDI")
        """

        self.supertype = supertype
        self.length = length
        self.method = method
        self.cutoff = cutoff

        self.errors: List[ErrorType] = []

    def get_table_template(self):
        raise NotImplementedError()

    def predict(self, sequence: str) -> List[MHCIEpitope]:
        results = list()

        for allele in self.supertype:
            output, errors = run_mhci_prediction_process(self.method, allele, self.length, sequence)

            if errors:
                self.errors.append({'allele': allele, 'errors': errors})
                continue

            _, rows = output.split('\n', 1)

            results_list = self.parse_results_table(rows)

            results.extend((MHCIEpitope(**r) for r in results_list if r['percentile'] > self.cutoff))

        return results

    def parse_results_table(self, results_table: str) -> List[dict]:
        template = self.get_table_template()

        parser = ttp(data=results_table, template=template)
        parser.parse()

        parsed_rows = parser.result(structure='flat_list')

        return parsed_rows


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
