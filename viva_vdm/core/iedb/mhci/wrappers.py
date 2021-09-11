import mhcflurry
from typing import List
from seqpredictor import MHCBindingPredictions
from util import InputData, OneSequenceInput
from .constants import MhcISupertypes, PredictionMethods
from .models import MHCIEpitope


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
            >>> from viva_vdm.core.iedb.mhci.wrapper import MhcINetMhcPan
            >>> prediction_supertype = MhcISupertypes.A1
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


class MhcINetMhcPan(MHCIPredictorBase):
    def predict(self, sequence: str) -> List[MHCIEpitope]:
        """
        This is the implementation of the prediction method for NetMHCPan.

        :param sequence: A protein sequences to predict epitopes for.
        :type sequence: str

        :return: A list of epitopes with IEDB percentile ranking that is equal to, or less than the defined cutoff.
        """

        results = list()
        input_protein = OneSequenceInput(sequence)

        for allele in self.supertype.value:
            input_data = InputData(
                version=self.version,
                method=self.method.value,
                mhc=allele,
                hla_seq=None,
                length=self.length,
                proteins=input_protein,
            )

            predictions = MHCBindingPredictions(input_data).predict(input_data.input_protein.as_amino_acid_text())
            predictions = [
                MHCIEpitope(sequence=hit[0], percentile=hit[3]) for hit in predictions[0][2][0] if hit[3] <= self.cutoff
            ]
            results.extend(predictions)

        return results


class MhcINetMhcPanEL(MhcINetMhcPan):
    ...


class MhcIPickpocket(MHCIPredictorBase):
    def predict(self, sequence: str) -> List[MHCIEpitope]:
        """
        This is the implementation of the prediction method for Pickpocket.

        :param sequence: A protein sequences to predict epitopes for.
        :type sequence: str

        :return: A list of epitopes with IEDB percentile ranking that is equal to, or less than the defined cutoff.
        """

        results = list()
        input_protein = OneSequenceInput(sequence)

        for allele in self.supertype.value:
            input_data = InputData(
                version=self.version,
                method=self.method.value,
                mhc=allele,
                hla_seq=None,
                length=self.length,
                proteins=input_protein,
            )

            predictions = MHCBindingPredictions(input_data).predict(input_data.input_protein.as_amino_acid_text())
            predictions = [
                MHCIEpitope(sequence=sequence[pos : pos + self.length], percentile=hit[1])  # noqa: E203
                for pos, hit in enumerate(predictions[0][2][0])
                if hit[1] <= self.cutoff
            ]
            results.extend(predictions)

        return results


class MhcFlurry(MHCIPredictorBase):
    def predict(self, sequence: str) -> List[MHCIEpitope]:
        """
        This is the implementation of the prediction method for Mhcflurry. This is not part of IEDB.
        https://github.com/openvax/mhcflurry

        :param sequence: A protein sequences to predict epitopes for.
        :type sequence: str

        :return: A list of epitopes with IEDB percentile ranking that is equal to, or less than the defined cutoff.
        """

        predictor = mhcflurry.Class1PresentationPredictor.load()

        results = predictor.predict_sequences(
            sequences=sequence,
            alleles=self.supertype.value,
            result="filtered",
            comparison_quantity="affinity_percentile",
            filter_value=self.cutoff,
        ).to_dict(orient="records")

        return [MHCIEpitope(sequence=hit.get("peptide"), percentile=hit.get("affinity_percentile")) for hit in results]
