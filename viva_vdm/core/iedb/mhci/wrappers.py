from typing import List
from seqpredictor import MHCBindingPredictions
from util import InputData, OneSequenceInput
from .constants import MhcISupertypes, PredictionMethods


class MHCIPredictorBase(object):
    def __init__(
        self,
        *,
        supertypes: List[MhcISupertypes],
        method: PredictionMethods = PredictionMethods.NETMHCPAN,
        length: int = 9,
        cutoff: float = 1.00,
    ):
        """
        This constructor is common for all MHC I prediction methods. It is recommended to not use this directly,
        but through the factory.

        :param supertypes: A list of pre-defined MHC I supertypes.
        :param method: One of the pre-defined MHC I prediction methods (default: NETMHCPAN).
        :param length: The length of the generated epitopes (default: 9).
        :param cutoff: The IEDB percentile cutoff (default: 1%).

        :type supertypes: List[MhcISupertypes]
        :type method: PredictionMethods
        :type length: int
        :type cutoff: float

        Example:
            >>> from viva_vdm.core.iedb.mhci.constants import MhcISupertypes, PredictionMethods
            >>> from viva_vdm.core.iedb.mhci.wrapper import MhcINetMhcPan
            >>> prediction_supertypes = [MhcISupertypes.A1, MhcISupertypes.A2]
            >>> predictor = MhcINetMhcPan(prediction_supertypes)
            >>> results = predictor.predict("MDSNTVSSFQDI")
        """

        self.version = '20130222'
        self.supertypes = supertypes
        self.length = length
        self.method = method
        self.cutoff = cutoff

    def predict(self, sequences: List[str]):
        ...


class MhcINetMhcPan(MHCIPredictorBase):
    def predict(self, sequence: str):
        """
        This is the implementation of the prediction method for NetMHCPan.

        :param sequence: A protein sequences to predict epitopes for.
        :type sequence: str

        :return:
        """
        results = list()

        for supertype in self.supertypes:
            input_protein = OneSequenceInput(sequence)

            for allele in supertype.value:
                input_data = InputData(
                    version=self.version,
                    method=self.method.value,
                    mhc=allele,
                    hla_seq=None,
                    length=self.length,
                    proteins=input_protein,
                )

                predictions = MHCBindingPredictions(input_data).predict(input_data.input_protein.as_amino_acid_text())
                results.append(predictions)

        return results
