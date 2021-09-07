from typing import List
from itertools import product
from seqpredictor import MHCBindingPredictions
from util import InputData, OneSequenceInput
from .constants import MhcISupertypes, PredictionMethods


class MHCIPredictorBase(object):
    def __init__(self, supertypes: List[MhcISupertypes], length: int, method: PredictionMethods):
        self.version = '20130222'
        self.supertypes = supertypes
        self.length = length
        self.method = method

    def predict(self, sequences: List[str]):
        ...


class MHCIPredictorANN(MHCIPredictorBase):
    def predict(self, sequences: List[str]):
        results = list()

        for sequence, supertype in product(sequences, self.supertypes):
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
