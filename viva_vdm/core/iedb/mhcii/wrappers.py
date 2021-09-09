from typing import List

from mhcii_predictor import MhciiPredictor
from .constants import MhcIISupertypes, PredictionMethods
from .models import MHCIIEpitope


class MHCIIPredictorBase(object):
    def __init__(
        self,
        *,
        supertype: MhcIISupertypes,
        method: PredictionMethods = PredictionMethods.NETMHCIIPAN,
        length: int = 9,
        cutoff: float = 1.00,
    ):
        """
        This constructor is common for all MHCII prediction methods. It is recommended to not use this directly,
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
            >>> from viva_vdm.core.iedb.mhcii.constants import MhcIISupertypes, PredictionMethods
            >>> from viva_vdm.core.iedb.mhcii.wrapper import MhcINetMhcPan
            >>> prediction_supertype = MhcIISupertypes.A1
            >>> predictor = MhcINetMhcPan(prediction_supertype)
            >>> results = predictor.predict("MDSNTVSSFQDI")
        """

        self.version = '20130222'
        self.supertype = supertype
        self.length = length
        self.method = method
        self.cutoff = cutoff

    def predict(self, sequence: str):
        ...


class MhcIINetMhcPan(MHCIIPredictorBase):
    def predict(self, sequence: str) -> List[MHCIIEpitope]:
        """
        This is the implementation of the prediction method for NetMHCPan.

        :param sequence: A protein sequences to predict epitopes for.
        :type sequence: str

        :return: A list of epitopes with IEDB percentile ranking that is equal to, or less than the defined cutoff.
        """

        allele_count = len(self.supertype.value)
        predictions = MhciiPredictor(self.method.value, self.supertype.value, [self.length] * allele_count).predict(
            [sequence]
        )

        return predictions
